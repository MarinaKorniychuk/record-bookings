import calendar
import datetime
import time

from datetime import timedelta

import httplib2
import logging
import pygsheets
from dateutil import rrule

from constants import CLIENT_SECRET_PATH
from utils.date_helper import get_date
from clients.http_client import make_custom_http
from utils.parse_bookings import read_bookings_from_file, process_bookings_data
from utils.spreadsheet_operations import get_worksheet_name_by_month, open_or_create_worksheet, \
    get_cell_address_by_date, update_range_with_values, update_cell_with_value

logger = logging.getLogger('record.bookings')


def read_and_process_booking_records(filename):
    # load all records from spreadsheet
    booking_records = read_bookings_from_file(filename)

    # calculate final amount without commission and daily profit
    processed_records = process_bookings_data(booking_records)
    return processed_records


def record_profits_to_spreadsheet(spreadsheet, records, skipped):
    worksheets = {}  # dict to store opened worksheets for different months (worksheet's name is a key)

    for _, record in records.iterrows():
        try:
            start_time = time.time()

            start_date = get_date(record['arrival_date'])
            end_date = get_date(record['leaving_date']) - timedelta(days=1)  # date of last staying day

            # iterate over every month of booking record
            # example: for record with dates `2022.12.28` - `2023.02.04` would iterate over the following values:
            #          month_date [`2022.12.01`, `2023.01.01`, `2023.02.01`]
            # the day of `month_date` doesn't matter, we only need month value to determine worksheet
            # this allows to complete recording for every month that is covered in booking period
            for month_date in rrule.rrule(
                    rrule.MONTHLY,
                    dtstart=datetime.date(start_date.year, start_date.month, 1),
                    until=end_date
            ):
                worksheet_month = month_date.month
                worksheet_year = month_date.year
                worksheet_name = get_worksheet_name_by_month(month_date)

                if not worksheets.get(worksheet_name):
                    open_or_create_worksheet(worksheet_name, spreadsheet, worksheets)

                # default border values for a range of cells (sets right and left border)
                # these values are changed later if booking period starts and ends in different months.
                border_values = [1, 1, 1, 1]

                # define call addresses of range for CURRENT ITERATION month
                if start_date.month == worksheet_month:
                    start_range_date = start_date
                else:
                    start_range_date = datetime.date(worksheet_year, worksheet_month, 1)
                    border_values[3] = 0

                _, start_cell = get_cell_address_by_date(start_range_date, record)

                if end_date.month == worksheet_month:
                    end_range_date = end_date
                else:
                    end_range_date = datetime.date(
                        worksheet_year,
                        worksheet_month,
                        calendar.monthrange(worksheet_year, worksheet_month)[1]
                    )
                    border_values[1] = 0

                _, end_cell = get_cell_address_by_date(end_range_date, record)

                price_values = [[record['daily_amount']] * ((end_range_date - start_range_date).days + 1)]
                update_range_with_values(start_cell, end_cell, worksheets[worksheet_name], price_values, border_values)

            # find and fill final_amount cell with value
            final_amount_cell_address, _ = get_cell_address_by_date(start_date, record)
            update_cell_with_value(
                final_amount_cell_address, record['final_amount'],
                worksheets[get_worksheet_name_by_month(start_date)]
            )

            logger.info(
                f'{record["source"]}: {record["category"]} [{start_date} - {get_date(record["leaving_date"])}] '
                f'profit: {record["final_amount"]} ({record["days"]} day(s) for {record["daily_amount"]}) '
                f'({format(time.time() - start_time, ".2f")}s).\n'
            )

            time.sleep(2)

        except httplib2.HttpLib2Error as error:
            logger.error(f'Caught the following error: {error}')

            skipped.append(record)
            continue

    logger.info(f'{spreadsheet.title} IS DONE\n')


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
            record_profits_to_spreadsheet(spreadsheet, records.head, skipped)
        except pygsheets.SpreadsheetNotFound:
            logger.warning(f'{spreadsheet_id} spreadsheet not found, skip.')
            pass
        except httplib2.HttpLib2Error as error:
            logger.error(f'Could not open {spreadsheet_id} spreadsheet: {error}')

    logger.info(f'Finished recording data at {datetime.datetime.now().time()}\n')

    logger.info(f'SKIPPED RECORDS: \n{skipped}')

def record_bookings(filepath):
    processed_data = read_and_process_booking_records(filepath)
    update_google_spreadsheets(processed_data)


# 28.12.2022 - 06.01.2023 /Users/marina.korniychuk/Downloads/19057_bookings_20230106193908_1.xlsx
# 29.11.2022 - 06.01.2023 /Users/marina.korniychuk/Downloads/19057_bookings_20230107002759_1.xlsx
# 14.12.2022 - 27.12.2022 /Users/marina.korniychuk/Downloads/19057_bookings_20230107031414_1.xlsx
