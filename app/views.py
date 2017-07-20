from flask import render_template, redirect, url_for
from app import app, db, models
from .utils import update_all_weather_reports
# from datetime import datetime
# import requests
# from key import GOOGLE_API_KEY
# from .parsers import parse_forecast_day, parse_forecast_date, parse_percent_precipitation
# from sqlalchemy.orm.exc import MultipleResultsFound


def log_error(message):
    print('!!!!!!!!!!!!!!!!!!!! Error: %s !!!!!!!!!!!!!!!!!!!!' % message)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new/')
def get_new_reports():

    update_all_weather_reports()

    return redirect(url_for('index'))


@app.route('/reports/')
def display_reports():
    reports = models.WeatherReport.query.all()
    return render_template('forecasts.html',
                           reports=reports)
