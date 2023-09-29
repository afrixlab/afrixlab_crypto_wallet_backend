from datetime import timedelta, datetime

from dateutil.parser import parse
from dateutil.parser import ParserError

from apps.utils.exceptions import CustomException


class DateTime:
    @staticmethod
    def format_date_and_time_to_readable_format(date_obj) -> str:
        _format = "%d %B, %Y %H:%M%p (UTC+0)"
        return date_obj.strftime(_format)

    @staticmethod
    def get_difference_between_two_dates_in_secs(later_date, earlier_date):
        return (later_date - earlier_date).total_seconds()

    @staticmethod
    def convert_seconds_to_hr_min(seconds: int) -> str:
        hr = seconds // (60 * 60)
        mins = (seconds - (hr * 3600)) // 60
        secs = seconds - ((hr * 3600) + (mins * 60))
        time_str = ""
        if hr:
            time_str += f"{hr} Hr{'s' if hr > 1 else ''} "
        if mins:
            time_str += f"{mins} Min{'s' if mins > 1 else ''} "
        if secs:
            time_str += f"{secs} Sec{'s' if secs > 1 else ''} "
        return time_str.strip()

    @staticmethod
    def add_date(
        date,
        minutes: int,
    ):
        # keeping this for breaking changes
        return date + timedelta(minutes=minutes)

    @staticmethod
    def add_timedelta(date, offset: int, time_unit="minute"):
        supported_time_unit = {
            "minutes": 0,
            "hours": 0,
            "microseconds": 0,
            "days": 0,
            "milliseconds": 0,
            "weeks": 0,
        }
        assert time_unit in supported_time_unit.keys()
        supported_time_unit[time_unit] = offset
        return date + timedelta(**supported_time_unit)

    @staticmethod
    def natural_time(minutes: int):
        if minutes < 60:
            return "%s minutes" % str(minutes)
        elif 60 < minutes < 1440:
            return "%s hour(s) %s" % str(minutes // 60)
        elif minutes > 1440:
            return "%s day(s)" % str(minutes // 1440)

    @staticmethod
    def natural_date(minutes: int):
        if minutes < 60:
            return "%s minutes" % str(minutes)
        elif 60 < minutes < 1440:
            return "%s hour(s) %s minute(s)" % (str(minutes // 60), str(minutes % 60))
        elif minutes > 1440:
            return "%s day(s) %s hour(s) %s minute(s)" % (
                str(minutes // 1440),
                str((minutes % 1440) // 60),
                str(minutes % 60),
            )

    @staticmethod
    def to_seconds(time_type, value):
        if isinstance(value, (int, float)):
            if time_type == "hours":
                value *= 3600
                return value
            elif time_type == "minutes":
                value *= 60
                return value
            else:
                raise ValueError("Invalid time type")
        else:
            raise TypeError("value must be an integer value_type")

    @staticmethod
    def string_to_datetime(date_string, *, _type="datetime") -> datetime:
        try:
            if _type == "datetime":
                return parse(date_string)
            elif _type == "date":
                return parse(date_string)
        except ParserError:
            raise CustomException(
                message="String to Datetime error",
                errors=["errors parsing date from string %s" % date_string],
            )
