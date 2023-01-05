from datetime import datetime


def calculate_amount_of_days(start, end):
    start_d = datetime.strptime(start, "%d.%m.%Y %H:%M").date()
    end_d = datetime.strptime(end, "%d.%m.%Y %H:%M").date()
    return (end_d - start_d).days
