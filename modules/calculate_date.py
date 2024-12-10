from datetime import datetime
from dateutil.relativedelta import relativedelta

def today():
    return datetime.now().strftime("%Y-%m-%d")

def next_day(date):
    return (datetime.strptime(date, "%Y-%m-%d") + relativedelta(days=1)).strftime("%Y-%m-%d")

def date_iterator(start_date: str, last_date: str):
    prev_date = datetime.strptime(start_date, "%Y-%m-%d")
    cur_date = prev_date + relativedelta(months=1)
    last_date = datetime.strptime(last_date, "%Y-%m-%d")

    while cur_date < last_date:
        yield (prev_date.strftime("%Y-%m-%d"), cur_date.strftime("%Y-%m-%d"))
        prev_date = cur_date + relativedelta(days=1)
        cur_date += relativedelta(months=1)

    yield (prev_date.strftime("%Y-%m-%d"), last_date.strftime("%Y-%m-%d"))