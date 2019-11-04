from flask import current_app
from typing import List, Tuple
import datetime
from dateutil.relativedelta import relativedelta


class DateRange:
    start: datetime.datetime
    end: datetime.datetime

    def __init__(self, start: datetime.datetime, end: datetime.datetime):
        self.start = start
        self.end = end

    @classmethod
    def for_today(cls):
        return DateRange.for_a_day(datetime.datetime.today())

    @classmethod
    def for_yesterday(cls):
        return DateRange.for_a_day(yesterday())

    @classmethod
    def for_a_day(cls, date: datetime.date):
        return DateRange.of_dates(date, date)

    @classmethod
    def of_dates(cls, start: datetime.date, end: datetime.date):
        start = datetime.datetime(start.year, start.month, start.day, 0, 0, 0)
        end = datetime.datetime(end.year, end.month, end.day, 23, 59, 59)
        return DateRange(start, end)

    def get_duration_in_days(self) -> int:
        return (self.end - self.start).days

    def get_dates(self) -> List[datetime.datetime]:
        d = self.get_duration_in_days()
        dates = []
        for i in range(d + 1):
            dates.append(self.start + datetime.timedelta(days=i))
        return dates

    def contains_today(self):
        return self.contains(datetime.datetime.today().date())

    def contains(self, date: datetime.date):
        return self.start.date() <= date <= self.end.date()

    def is_single_day(self):
        return self.get_duration_in_days() is 0

    def is_week(self):
        return 0 < self.get_duration_in_days() < 15

    def is_month(self):
        return 15 < self.get_duration_in_days() < 32

    def get_first_dates_of_months(self) -> List[datetime.datetime]:
        dates = []
        date = self.start
        while date <= self.end:
            dates.append(datetime.datetime(date.year, date.month, 1))
            date += relativedelta(months=1)
        return dates

    def get_first_hours(self) -> List[datetime.datetime]:
        dates = []
        date = self.start
        while date <= self.end:
            dates.append(datetime.datetime(date.year, date.month, date.day, date.hour, 0, 0))
            date += relativedelta(hours=1)
        return dates

    def __to_date_dict__(self):
        return {
            'start': format_date(self.start.date()),
            'end': format_date(self.end.date())
        }

    def __to_dict__(self):
        return {
            'start': format_datetime(self.start),
            'end': format_datetime(self.end)
        }


def format_datetime(value: datetime.datetime):
    if value is None:
        return None
    elif type(value) == str:
        return value
    return value.strftime("%Y-%m-%d %H:%M:%S")


def format_date(value: datetime.date):
    return value.strftime("%Y-%m-%d")


def yesterday() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=1)


def get_start_end_for_a_date(date: datetime.date) -> DateRange:
    return DateRange.for_a_day(date)


def difference_btw_old_and_new_entry(entry, updated_entry):
    diff_keys = [key for key in entry if entry[key] != updated_entry[key]]
    entry_logs_key = {}
    entry_logs_old = {}
    entry_logs_new = {}

    i = 0
    for key in diff_keys:
        if key == 'created_at':
            continue

        entry_logs_key[i] = key
        entry_logs_old[key] = entry[key]
        entry_logs_new[key] = updated_entry[key]
        i = i + 1

    return entry_logs_key, entry_logs_new, entry_logs_old


def get_date_from_mysql_format(date: str) -> datetime.date:
    date_format = "%Y-%m-%d"
    return datetime.datetime.strptime(date, date_format).date()


def get_date_time_from_mysql_format(date: str) -> datetime.datetime:
    date_format = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strptime(date, date_format)


def date_to_datetime(date: datetime.date) -> datetime.datetime:
    return datetime.datetime(year=date.year, month=date.month, day=date.day)


def log(*argv):
    for arg in argv:
        current_app.logger.info(msg=arg)


def float_to_money(value):
    return float("{0:.2f}".format(value))


def get_time_string_file_name(filename):
    import time
    from werkzeug.utils import secure_filename
    stamp = time.strftime("%Y%m%d_%H%M%S")
    filename = secure_filename(filename)
    split = filename.rsplit('.', 1)
    return "{}_{}.{}".format(split[0], stamp, split[1])


ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
