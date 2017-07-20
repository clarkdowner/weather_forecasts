from datetime import datetime
from app import models
from .api import _google_maps_api_request, _national_weather_api_request


def parse_forecast_day(name):
    """
    Turn National Weather service 'name' property into use-able day of week

    :param name: forecast name from NWS JSON
    :return: day of the week
    """
    lower = name.lower()
    if lower == 'today' or lower == 'tonight' or lower == 'this afternoon':
        return datetime.today().strftime("%A")
    else:
        split = name.split(" ")
        return split[0]


def parse_forecast_date(start_time):
    split = start_time.split("T")
    return split[0]


def parse_percent_precipitation(detailed_forecast):
    """
    As of 07/20/2017 the National Weather Service does not return precipitation as it's own field,
    instead this function finds the chance of precipitation from the detailed forecast the do return

    :param detailed_forecast: detailed forecast from NWS JSON
    :return: percent chance of precipitation
    """
    lower = detailed_forecast.lower()
    key = 'chance of precipitation is '
    try:
        slice_index = lower.index(key)
    except ValueError:
        return '0'

    chop_forecast = lower[slice_index:]
    try:
        percent_index = chop_forecast.index('%')
    except ValueError:
        # TODO: logging
        # log_parse_error('finding precipitation')
        return '0'
    length = len(key)
    percent = chop_forecast[length:percent_index]
    return percent


def get_lat_and_long(zip_code):  # TODO: figure out if this is the right place for this, doesn't seem to belong to model
    """
    Return latitude and longitude for a given zip code

    :param zip_code: zip code
    :return: coordinates to four decimal places
    """
    geo_data = _google_maps_api_request(zip_code)

    lat = geo_data['results'][0]['geometry']['location']['lat']
    long = geo_data['results'][0]['geometry']['location']['lng']

    latitude = round(lat, 4)
    longitude = round(long, 4)

    return latitude, longitude


def get_location_forecasts(latitude,
                           longitude):  # TODO: figure out if this is the right place for this, doesn't seem to belong to model
    """
    Get seven days of forecasts for a given coordinate pair

    :param latitude: latitude to four decimals
    :param longitude: longitude to four decimals
    :return: array of forecasts
    """
    data = _national_weather_api_request(latitude, longitude)
    forecasts = data['properties']['periods']

    return forecasts


def decorate_forecast(forecast, zip):
    """
    Decorate forecast with properties necessary for matching with existing record

    :param forecast: forecast
    :param zip: zip
    :return: forecast decorated with 'zip', 'forecast_day', 'is_daytime', and 'is_current' properties
    """
    forecast['zip'] = zip
    forecast['forecast_day'] = parse_forecast_day(forecast['name'])
    forecast['is_daytime'] = forecast['isDaytime']

    if forecast['number'] is 1:
        forecast['is_current'] = True
    else:
        forecast['is_current'] = False

    return forecast


def update_all_weather_reports():
    """
    Find up-to-date seven day forecasts for all locations, and update existing forecast records or add new records

    :return: none
    """

    locations = models.get_all_locations()

    for location in locations:
        if location.latitude is None or location.longitude is None:
            latitude, longitude = get_lat_and_long(location.zip)
            models.update_location(location, latitude, longitude)

        forecasts = get_location_forecasts(location.latitude, location.longitude)

        for forecast in forecasts:
            forecast = decorate_forecast(forecast, location.zip)
            models.commit_forecast(forecast)

    print('$$')

