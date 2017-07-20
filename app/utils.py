from datetime import datetime
from app import models
from .api import _google_maps_api_request, _national_weather_api_request


def parse_forecast_day(name):
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

    :param zip_code:
    :return:
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

    :param lat:
    :param long:
    :return: an array of forecasts
    """
    data = _national_weather_api_request(latitude, longitude)
    forecasts = data['properties']['periods']

    return forecasts


def decorate_forecast(forecast, zip):
    forecast['zip'] = zip
    forecast['forecast_day'] = parse_forecast_day(forecast['name'])
    forecast['is_daytime'] = forecast['isDaytime']

    if forecast['number'] is 1:
        forecast['is_current'] = True
    else:
        forecast['is_current'] = False

    return forecast


def update_all_weather_reports():

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

