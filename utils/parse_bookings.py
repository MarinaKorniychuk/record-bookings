import math

import pandas as pd

from data.apartments import SEREBRYANICHESKIY_APARTMENTS, RADIK_APARTMENTS, DINARA_APARTMENTS
from constants import BNOVA_SHEET_NAME, COMMISSION_MAP, RADIK_SPREADSHEET_ID, DINARA_SPREADSHEET_ID, \
    SEREBRYANICHESKIY_SPREADSHEET_ID
from utils.date_helper import calculate_amount_of_days


def calculate_profit_amount(row):
    """Maps source (источник бронирования) with commission value and calculated final profit amount"""
    return float(row['total_amount']) * (1 - COMMISSION_MAP[row['source']])


def calculate_daily_amount(row):
    return math.floor(float(row['final_amount']) / row['days'])


def process_bookings_data(bookings):
    """Adds final_amount, days and daily_amount columns to records dataset
    Split all data in three datasets based on spreadsheet they belong to
    Return dict where key is Google spreadsheet id and value id dataset with booking records."""
    bookings['final_amount'] = bookings.apply(lambda row: calculate_profit_amount(row), axis=1)
    bookings['days'] = bookings.apply(lambda row: calculate_amount_of_days(row['arrival_date'], row['leaving_date']), axis=1)
    bookings['daily_amount'] = bookings.apply(lambda row: calculate_daily_amount(row), axis=1)

    data = {
        SEREBRYANICHESKIY_SPREADSHEET_ID: bookings.query("category in @SEREBRYANICHESKIY_APARTMENTS"),
        DINARA_SPREADSHEET_ID: bookings.query("category in @DINARA_APARTMENTS"),
        RADIK_SPREADSHEET_ID: bookings.query("category in @RADIK_APARTMENTS"),
    }

    return data


