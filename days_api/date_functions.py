"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    '''converts string of format DAY.MONTH.YEAR to a datetime object'''
    try:
        return datetime.strptime(date_val, "%d.%-m.%Y")
    except ValueError as e:
        raise ValueError("Unable to convert value to datetime.") from e


def get_days_between(first: datetime, last: datetime) -> int:
    if isinstance(first, datetime) is False or isinstance(last, datetime) is False:
        raise TypeError("Datetimes required.")
    return (last - first).days


def get_day_of_week_on(date_val: datetime) -> str:
    if isinstance(date_val, datetime) is False:
        raise TypeError("Datetime required.")
    return date_val.strftime('%A')


def get_current_age(birthdate: date) -> int:
    pass
