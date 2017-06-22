from datetime import datetime


def log_parse_error(message):
    print('!!!!!!!!!!!!!!!!!!!!!!!!! Error %s. !!!!!!!!!!!!!!!!!!!!!!!!!' % message)


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
        log_parse_error('finding precipitation')
        return '0'
    length = len(key)
    percent = chop_forecast[length:percent_index]
    return percent
