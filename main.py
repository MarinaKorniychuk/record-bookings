import argparse
import pygsheets

from constants import CLIENT_SECRET_PATH
from utils.parse_bookings import read_bookings_from_file, process_bookings_data

gc = pygsheets.authorize(CLIENT_SECRET_PATH)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='record-bookings',
        description='Fills the bookings spreadsheet with bookings from Bnova spreadsheet.',
    )
    parser.add_argument('filename')  # required positional argument
    return parser.parse_args()


def record_bookings():
    filename = parse_args().filename

    # load all records from spreadsheet
    bookings = read_bookings_from_file(filename)

    # calculate final amount without commission
    processed_data = process_bookings_data(bookings)


if __name__ == "__main__":
    record_bookings()
