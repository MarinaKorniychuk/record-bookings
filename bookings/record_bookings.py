import calendar
import datetime
import logging
import time

from datetime import timedelta
from dateutil import rrule

import httplib2

from pygsheets import SpreadsheetNotFound, RequestError, IncorrectCellLabel, WorksheetNotFound

from clients.bnova_client import BnovaClient
from clients.google_client import GoogleClient
from utils.configuration import get_spreadsheets_config, get_bookings_config
from utils.date_helper import get_date
from utils.log_error import log_error
from utils.process_bookings_data import process_bookings_data
from utils.spreadsheet_operations import get_worksheet_name_by_month, open_or_create_worksheet, \
    get_profit_cell_address_by_date, update_range_with_values, update_cell_with_value

logger = logging.getLogger('record.bookings')


def record_profits_to_spreadsheet(spreadsheet, records, skipped):
    """Here happens recording of bookings data to Google spreadsheet
    Bookings are recorded one by one. Booking which booking period overlaps with more than one different months,
    divided into parts and recorded one after another into different worksheets
    """
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

                _, start_cell = get_profit_cell_address_by_date(start_range_date, record)

                if end_date.month == worksheet_month:
                    end_range_date = end_date
                else:
                    end_range_date = datetime.date(
                        worksheet_year,
                        worksheet_month,
                        calendar.monthrange(worksheet_year, worksheet_month)[1]
                    )
                    border_values[1] = 0

                _, end_cell = get_profit_cell_address_by_date(end_range_date, record)

                price_values = [[record['daily_amount']] * ((end_range_date - start_range_date).days + 1)]
                update_range_with_values(start_cell, end_cell, worksheets[worksheet_name], price_values, border_values)

            # find and fill final_amount cell with value
            final_amount_cell_address, _ = get_profit_cell_address_by_date(start_date, record)
            update_cell_with_value(
                final_amount_cell_address, record['final_amount'],
                worksheets[get_worksheet_name_by_month(start_date)]
            )

            logger.info(
                f'{record["source"]}: {record["category"]} [{start_date} - {get_date(record["leaving_date"])}] '
                f'полный приход: {record["final_amount"]}р ({record["days"]} {"день" if record["days"] == 1 else "дня"} '
                f'по {record["daily_amount"]}р).\n'
            )

            time.sleep(2)

        except (httplib2.HttpLib2Error, RequestError, IncorrectCellLabel) as error:
            log_error(error)
            skipped.append(record)
            continue

    logger.info(f'Закончено заполнение таблицы "{spreadsheet.title}".\n')


def update_google_spreadsheets(data, gc):
    """For each spreadsheet in dataset call recording to Google spreadsheet"""
    logger.debug(f'Started recording data at {datetime.datetime.now().time()}\n')

    skipped = []
    # recording is done for each spreadsheet one by one as they are specified in data
    for spreadsheet_title, records in data.items():
        try:
            # open spreadsheet by its id (ids stored in constants.py file)
            spreadsheet = gc.open(spreadsheet_title)
            record_profits_to_spreadsheet(spreadsheet, records, skipped)
        except (SpreadsheetNotFound, RequestError, httplib2.HttpLib2Error) as error:
            log_error(error)
            skipped.append(records)

    logger.debug(f'Finished recording data at {datetime.datetime.now().time()}\n')

    logger.info(f'Пропущенные записи: \n{skipped}')


def run(arrival_from, arrival_to, spreadsheets_config):
    """Create Google and Bnova client
    Get all configurations, retrieve and process bookings from Bnova
    Run updating Google spreadsheets function
    """
    gc = GoogleClient().gc
    bc = BnovaClient()

    if not gc:
        return

    try:
        bookings_config = get_bookings_config(gc)
    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        log_error(error)
        return

    raw_data = bc.get_bookings_data(arrival_from, arrival_to)
    bookings_data = process_bookings_data(raw_data, spreadsheets_config, bookings_config)

    update_google_spreadsheets(bookings_data, gc)
