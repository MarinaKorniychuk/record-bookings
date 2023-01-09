import datetime
import httplib2
import logging
import pygsheets

from constants import CLIENT_SECRET_PATH
from utils.http_client import make_custom_http
from utils.parse_bookings import read_bookings_from_file, process_bookings_data
from utils.spreadsheet_operations import record_booking_records


logger = logging.getLogger('record.bookings')


def read_and_process_booking_records(filename):
    # load all records from spreadsheet
    booking_records = read_bookings_from_file(filename)

    # calculate final amount without commission and daily profit
    processed_records = process_bookings_data(booking_records)
    return processed_records


def update_google_spreadsheets(data):
    """Transfer records from dataset to Google spreadsheets"""
    gc = pygsheets.authorize(CLIENT_SECRET_PATH, http=make_custom_http())

    logger.info('Google API client: authorized.')
    logger.info(f'Started recording data at {datetime.datetime.now().time()}\n')

    skipped = []
    # recording is done for each spreadsheet one by one as they are specified in data
    for spreadsheet_id, records in data.items():
        try:
            # open spreadsheet by its id (ids stored in constants.py file)
            spreadsheet = gc.open_by_key(spreadsheet_id)
            record_booking_records(spreadsheet, records.head(1), skipped)
        except pygsheets.SpreadsheetNotFound:
            logger.warning(f'{spreadsheet_id} spreadsheet not found, skip.')
            pass
        except httplib2.HttpLib2Error as error:
            logger.error(f'Could not open {spreadsheet_id} spreadsheet: {error}')

    logger.info(f'Finished recording data at {datetime.datetime.now().time()}')

    logger.info(f'\nSKIPPED RECORDS: \n{skipped}')

def record_bookings(filepath, logger=None):
    processed_data = read_and_process_booking_records(filepath)
    update_google_spreadsheets(processed_data)


# 28.12.2022 - 06.01.2023 /Users/marina.korniychuk/Downloads/19057_bookings_20230106193908_1.xlsx
# 29.11.2022 - 06.01.2023 /Users/marina.korniychuk/Downloads/19057_bookings_20230107002759_1.xlsx
# 14.12.2022 - 27.12.2022 /Users/marina.korniychuk/Downloads/19057_bookings_20230107031414_1.xlsx
