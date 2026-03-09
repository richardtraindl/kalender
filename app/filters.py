

from datetime import datetime, date, timedelta
from .helper import gib_feiertag as helper_gib_feiertag


def calc_kw(dt):
    dt = date(dt.year, dt.month, dt.day)

    # Determine its Day of Week, D
    # Use that to move to the nearest Thursday (-3..+3 days)
    add = 4 - dt.weekday()
    dt += timedelta(days=add)

    # Note the year of that date, Y
    # Obtain January 1 of that year
    firstofyear = date(dt.year, 1, 1)

    # Get the Ordinal Date of that Thursday, DDD of YYYY-DDD
    ydays = (dt - firstofyear).days + 1

    # Then W is 1 + (DDD-1) div 7
    return int(1 + (ydays / 7))


def add_days(dt, days):
    return dt + timedelta(days=days)


def add_hours(dt, hours):
    return dt + timedelta(hours=hours)


def add_mins(dt, mins):
    return dt + timedelta(minutes=mins)


def gib_feiertag(dt):
    return helper_gib_feiertag(dt)
