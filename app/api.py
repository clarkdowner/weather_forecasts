import requests
from key import GOOGLE_API_KEY


def _google_maps_api_request(zip_code):
    api_request_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' \
                 % (zip_code, GOOGLE_API_KEY)
    response = requests.get(api_request_url)

    if response.status_code != 200:
        # TODO: logging
        # log_error('could not retrieve lat and long from Google for zip: %s' % zip_code)
        print('err')

    return response.json()


def _national_weather_api_request(latitude, longitude):
    api_request_url = 'https://api.weather.gov/points/%s,%s/forecast' % (latitude, longitude)
    response = requests.get(api_request_url)

    if response.status_code != 200:
        # TODO: logging
        # log_error('could not retrieve forecasts from National Weather Service for latitude: %s and longitude: %s' \
        #           % (latitude, longitude))
        print('err')

    return response.json()