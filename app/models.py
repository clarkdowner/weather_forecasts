from app import db
from datetime import datetime

from .utils import parse_forecast_date, parse_percent_precipitation, get_lat_and_long
from sqlalchemy.orm.exc import MultipleResultsFound


# foreign key relationships commented out
class Location(db.Model):
    __tablename__ = 'locations'

    zip = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # forecasts = db.relationship('WeatherReport', backref='location', lazy='dynamic')

    def __repr__(self):
        return "<Location(zip='%s', name='%s', latitude='%s', longitude='%s')>"\
               % (self.zip, self.name, self.latitude, self.longitude)


class WeatherReport(db.Model):
    __tablename__ = 'weather_reports'

    id = db.Column(db.Integer, primary_key=True)
    # zip = db.Column(db.String, db.ForeignKey('locations.zip'))
    zip = db.Column(db.String)
    forecast_day = db.Column(db.String)
    forecast_date = db.Column(db.String)
    temperature = db.Column(db.Integer)
    wind_speed = db.Column(db.String)
    icon_url = db.Column(db.String)
    percent_precipitation = db.Column(db.Integer)
    is_daytime = db.Column(db.Boolean)
    short_forecast = db.Column(db.String)
    detailed_forecast = db.Column(db.String)
    update_time = db.Column(db.DateTime)
    is_current_forecast = db.Column(db.Boolean)

    # locations = db.relationship(Location)

    def __repr__(self):
        return '''
            <WeatherReport(zip='%s', forecast_date='%s', forecast_day='%s', 
            is_daytime='%s', short_forecast='%s', update_time='%s')>
        ''' % (self.zip, self.forecast_date, self.forecast_day,
               self.is_daytime, self.short_forecast, self.update_time)


def add_weather_report(forecast):
    """
    Get latest Clubhouse Info record
    """
    weather_report_to_commit = WeatherReport(zip=forecast['zip'],
                                             forecast_day=forecast['forecast_day'],
                                             forecast_date=parse_forecast_date(forecast['startTime']),
                                             temperature=forecast['temperature'], wind_speed=forecast['windSpeed'],
                                             icon_url=forecast['icon'],
                                             percent_precipitation=parse_percent_precipitation \
                                                 (forecast['detailedForecast']),
                                             is_daytime=forecast['is_daytime'],
                                             short_forecast=forecast['shortForecast'],
                                             detailed_forecast=forecast['detailedForecast'],
                                             update_time=datetime.utcnow(),
                                             is_current_forecast=['is_current'])

    db.session.add(weather_report_to_commit)
    db.session.commit()


def update_weather_report(report_to_update, forecast):
    """
    Get latest Clubhouse Visit Info record
    """
    report_to_update.forecast_date = parse_forecast_date(forecast['startTime'])
    report_to_update.temperature = forecast['temperature']
    report_to_update.wind_speed = forecast['windSpeed']
    report_to_update.icon_url = forecast['icon']
    report_to_update.percent_precipitation = parse_percent_precipitation(forecast['detailedForecast'])
    report_to_update.short_forecast = forecast['shortForecast']
    report_to_update.detailed_forecast = forecast['detailedForecast']
    report_to_update.update_time = datetime.utcnow()
    report_to_update.is_current_forecast = forecast['is_current']

    db.session.commit()


def update_location(location_to_update, latitude, longitude):
    location_to_update.latitude = latitude
    location_to_update.longitude = longitude

    db.session.commit()


def get_all_locations():
    """
    Get latest Clubhouse Media Info record
    """
    locations = db.session.query(Location).all()

    return locations


def get_all_weather_reports():
    """

    :return:
    """
    reports = db.session.query(WeatherReport).all()

    return reports


def commit_forecast(forecast):
    try:
        report = get_weather_report(forecast)

        if report is None:
            add_weather_report(forecast)
        else:
            update_weather_report(report, forecast)

    except MultipleResultsFound:
        # TODO: logging
        # log_error('duplicate results for for zip: %r, forecast_day: %r, is_daytime: %r' \
        #           % (forecast['zip'], forecast['forecast_day'], forecast['is_daytime']))
        print('##')


def get_weather_report(forecast):
    report = db.session.query(WeatherReport).filter(WeatherReport.zip == forecast['zip']). \
        filter(WeatherReport.forecast_day == forecast['forecast_day']). \
        filter(WeatherReport.is_daytime == forecast['is_daytime']).one_or_none()

    return report

