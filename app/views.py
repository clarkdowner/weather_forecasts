from flask import render_template, redirect, url_for
from app import app, db, models
from datetime import datetime
import requests
from key import GOOGLE_API_KEY
from .parsers import parse_forecast_day, parse_forecast_date, parse_percent_precipitation
from sqlalchemy.orm.exc import MultipleResultsFound


def log_error(message):
    print('!!!!!!!!!!!!!!!!!!!! Error: %s !!!!!!!!!!!!!!!!!!!!' % message)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new/')
def get_new_reports():
    locations = models.Location.query.all()
    for location in locations:

        if location.latitude is None or location.longitude is None:
            google_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' \
                         % (location.zip, GOOGLE_API_KEY)
            gr = requests.get(google_url)

            if gr.status_code != 200:
                log_error('could not retrieve lat and long from Google for %s' % location.name)
                return render_template('index.html')

            g_data = gr.json()
            location.latitude = round(g_data['results'][0]['geometry']['location']['lat'], 4)
            location.longitude = round(g_data['results'][0]['geometry']['location']['lng'], 4)
            db.session.commit()

        url = 'https://api.weather.gov/points/%s,%s/forecast' % (location.latitude, location.longitude)
        r = requests.get(url)

        if r.status_code != 200:
            log_error('could not retrieve forecast for %s from National Weather Service' % location.name)
            return render_template('index.html')

        data = r.json()
        forecasts = data['properties']['periods']

        for forecast in forecasts:
            zip = location.zip
            forecast_day = parse_forecast_day(forecast['name'])
            is_daytime = forecast['isDaytime']

            if forecast['number'] is 1:
                is_current = True
            else:
                is_current = False

            try:
                report = models.WeatherReport.query.filter(models.WeatherReport.zip == zip). \
                    filter(models.WeatherReport.forecast_day == forecast_day). \
                    filter(models.WeatherReport.is_daytime == is_daytime).one_or_none()

                if report is None:
                    wr = models.WeatherReport(zip=location.zip,
                                              forecast_day=forecast_day,
                                              forecast_date=parse_forecast_date(forecast['startTime']),
                                              temperature=forecast['temperature'], wind_speed=forecast['windSpeed'],
                                              icon_url=forecast['icon'],
                                              percent_precipitation=parse_percent_precipitation \
                                                  (forecast['detailedForecast']),
                                              is_daytime=is_daytime,
                                              short_forecast=forecast['shortForecast'],
                                              detailed_forecast=forecast['detailedForecast'],
                                              update_time=datetime.utcnow(),
                                              is_current_forecast=is_current)
                    db.session.add(wr)
                    db.session.commit()
                else:
                    report.forecast_date = parse_forecast_date(forecast['startTime'])
                    report.temperature = forecast['temperature']
                    report.wind_speed = forecast['windSpeed']
                    report.icon_url = forecast['icon']
                    report.percent_precipitation = parse_percent_precipitation(forecast['detailedForecast'])
                    report.short_forecast = forecast['shortForecast']
                    report.detailed_forecast = forecast['detailedForecast']
                    report.update_time = datetime.utcnow()
                    report.is_current_forecast = is_current
                    db.session.commit()

            except MultipleResultsFound:
                log_error('duplicate results for for zip: %r, forecast_day: %r, is_daytime: %r'\
                          % (zip, forecast_day, is_daytime))

    return redirect(url_for('index'))


@app.route('/reports/')
def display_reports():
    reports = models.WeatherReport.query.all()
    return render_template('forecasts.html',
                           reports=reports)
