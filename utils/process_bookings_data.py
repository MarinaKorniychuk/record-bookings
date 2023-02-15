import math

import pandas as pd

from constants import COMMISSION_MAP
from utils.date_helper import calculate_amount_of_days
from utils.log_error import log_error


def calculate_profit_amount(row):
    """Maps source (источник бронирования) with commission value and calculated final profit amount"""
    return math.floor(float(row['total_amount']) * (1 - COMMISSION_MAP[row['source']]))


def calculate_daily_amount(row):
    return math.floor(float(row['final_amount']) / row['days'])


def get_dataframe_from_raw_data(raw_data):
    df = pd.DataFrame.from_records(
        raw_data,
        columns=['source_id', 'arrival', 'departure', 'prices_rooms_total', 'initial_room_type_name']
    )

    column_names = ['source', 'arrival_date', 'leaving_date', 'total_amount', 'category']
    df = df.set_axis(column_names, axis=1, copy=False)

    df.loc[df["source"] == '356', "source"] = 'Ostrovok'
    df.loc[df["source"] == '14', "source"] = 'Sutochno'
    df.loc[df["source"] == '0', "source"] = 'Прямой'

    return df


def process_bookings_data(raw_data, spreadsheets_config, bookings_config):
    """Adds final_amount, days and daily_amount columns to records dataset
    Merge with config dataframe to add target spreadsheet and cell addresses to the records
    Split all data in three datasets based on spreadsheet they belong to
    Return dict where key is Google spreadsheet id and value id dataset with booking records."""

    bookings_df = get_dataframe_from_raw_data(raw_data)

    bookings_df['final_amount'] = bookings_df.apply(lambda row: calculate_profit_amount(row), axis=1)
    bookings_df['days'] = bookings_df.apply(lambda row: calculate_amount_of_days(row['arrival_date'], row['leaving_date']), axis=1)
    bookings_df['daily_amount'] = bookings_df.apply(lambda row: calculate_daily_amount(row), axis=1)

    cols = ['category']
    bookings_df = bookings_df.join(bookings_config.set_index(cols), on=cols)

    valid_bookings_df = bookings_df.dropna(subset=['category', 'spreadsheet', 'line1', 'line2'])

    invalid = pd.concat([bookings_df, valid_bookings_df]).drop_duplicates(keep=False)
    if len(invalid):
        invalid = invalid[['category', 'arrival_date']]
        log_error(f'Could not record the following bookings:\n\n{invalid}\n')

    data = dict()

    for _, record in spreadsheets_config.iterrows():
        spreadsheet_id = record['spreadsheet_id']
        data[record['spreadsheet_title']] = valid_bookings_df.query("spreadsheet == @spreadsheet_id")

    return data


