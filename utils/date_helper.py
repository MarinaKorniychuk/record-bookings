from datetime import datetime


def get_date(dt):
    return datetime.strptime(dt.split('+')[0], "%Y-%m-%d %H:%M:%S").date()


def calculate_amount_of_days(start, end):
    start_d = get_date(start)
    end_d = get_date(end)
    return (end_d - start_d).days
