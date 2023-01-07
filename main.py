import argparse
import httplib2
import logging
import pygsheets

from constants import CLIENT_SECRET_PATH
from utils.parse_bookings import read_bookings_from_file, process_bookings_data
from utils.spreadsheet_operations import record_booking_records


httplib2.debuglevel = 1

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='record-bookings',
        description='Fills the bookings spreadsheet with bookings from Bnova spreadsheet.',
    )
    parser.add_argument('filepath')  # required positional argument
    return parser.parse_args()


def read_and_process_booking_records(filename):
    # load all records from spreadsheet
    booking_records = read_bookings_from_file(filename)

    # calculate final amount without commission and daily profit
    processed_records = process_bookings_data(booking_records)
    return processed_records


def update_google_spreadsheets(data):
    gc = pygsheets.authorize(CLIENT_SECRET_PATH)
    print('Google API client: authorized.')

    for spreadsheet_id, records in data.items():
        spreadsheet = gc.open_by_key(spreadsheet_id)
        record_booking_records(spreadsheet, records)


if __name__ == "__main__":
    filepath = parse_args().filepath
    processed_data = read_and_process_booking_records(filepath)
    update_google_spreadsheets(processed_data)


if __name__ == "__main__":
    main()


# 28.12.2022 - 06.01.2023 /Users/marina.korniychuk/Downloads/19057_bookings_20230106193908_1.xlsx
# 29.11.2022 - 06.01.2023 /Users/marina.korniychuk/Downloads/19057_bookings_20230107002759_1.xlsx
