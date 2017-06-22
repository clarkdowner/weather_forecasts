from app import db


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
