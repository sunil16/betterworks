# Python program to Find day of
# the week for a given date
import datetime
import calendar


def find_day(date=None):
    day = datetime.datetime.strptime(str(date), '%Y-%m-%d').weekday()
    return (calendar.day_name[day])

def get_delta_date_and_day(delta=None):
    start_date = datetime.date.today() - datetime.timedelta(days=delta) # for demo purpose, analysing 5 days data only
    return (find_day(start_date),start_date)
