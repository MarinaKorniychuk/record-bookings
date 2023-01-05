import pandas as pd

from constants import BNOVA_SHEET_NAME, COMMISSION_MAP


def read_bookings_from_file(filename):
    bookings = pd.read_excel(
        filename,
        sheet_name=BNOVA_SHEET_NAME,
        usecols=['Источник', 'Дата брони', 'Заезд', 'Выезд', 'Категория', 'Итого']
    )
    column_names = ['source', 'booking_data', 'arrival_date', 'leaving_date', 'category', 'total_amount']
    bookings = bookings.set_axis(column_names, axis=1, copy=False)

    return bookings


def calculate_profit_amount(row):
    return row['total_amount'] * (1 - COMMISSION_MAP[row['source']])


def process_bookings_data(bookings):
    bookings['final_amount'] = bookings.apply(lambda row: calculate_profit_amount(row), axis=1)

    return bookings


