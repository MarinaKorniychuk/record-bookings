import logging
import time

from datetime import datetime

import httplib2

from pygsheets import RequestError, SpreadsheetNotFound, IncorrectCellLabel, WorksheetNotFound

from clients.google_client import GoogleClient
from utils.configuration import get_form_responses_worksheet, get_spreadsheets_config, get_expenses_config
from utils.date_helper import get_expense_date
from utils.log_error import log_error
from utils.process_expensess_data import get_processed_expenses_data
from utils.spreadsheet_operations import get_worksheet_name_by_month, open_or_create_worksheet, \
    get_expense_cell_address_by_date, update_expense_cell_value, update_cell_with_value

logger = logging.getLogger('record.bookings')


def record_expenses_to_spreadsheet(spreadsheet, records, response_worksheet, skipped):
    """Here happens recording of expenses data to Google spreadsheet
    Expenses are recorded one by one. Price is always recorded to the cell note with a comment.
    Multiple expenses can be written in the same cell, their amounts will be summarized and
    the note will reflect the list with  each expense's amount and comment.
    """
    worksheets = {}  # dict to store opened worksheets for different months (worksheet's name is a key)

    for _, record in records.iterrows():
        try:
            expense_date = get_expense_date(record['datetime'])

            worksheet_name = get_worksheet_name_by_month(expense_date)

            if not worksheets.get(worksheet_name):
                open_or_create_worksheet(worksheet_name, spreadsheet, worksheets)

            expense_cell_address = get_expense_cell_address_by_date(expense_date, record)
            update_expense_cell_value(expense_cell_address, record['amount'], record['note'], worksheets[worksheet_name])

            update_cell_with_value(f'P{record["rec_line"]}', 1, response_worksheet)

            logger.info(
                f'Трата от {expense_date} в размере {record["amount"]}р в категории {record["category"]} внесена в таблицу.\n'
            )

            time.sleep(2)


        except (httplib2.HttpLib2Error, RequestError, IncorrectCellLabel) as error:
            log_error(error)
            skipped.append(record)
            continue

    logger.info(f'Закончено заполнение таблицы "{spreadsheet.title}".\n')

def update_google_spreadsheets(data, gc):
    """For each spreadsheet in dataset call recording to Google spreadsheet"""
    logger.debug(f'Started recording data at {datetime.now().time()}\n')

    expenses_worksheet = get_form_responses_worksheet(gc)

    skipped = []
    # recording is done for each spreadsheet one by one as they are specified in data
    for spreadsheet_title, records in data.items():
        try:
            # open spreadsheet by its id (ids stored in constants.py file)
            spreadsheet = gc.open(spreadsheet_title)
            record_expenses_to_spreadsheet(spreadsheet, records, expenses_worksheet, skipped)
        except (SpreadsheetNotFound, RequestError, httplib2.HttpLib2Error) as error:
            log_error(error)
            skipped.append(records)


    logger.debug(f'Finished recording data at {datetime.now().time()}\n')

    logger.info(f'Пропущенные записи: \n{skipped}')


def run():
    """Create Google client
    Get all configurations, retrieve and process expenses data
    Run updating Google spreadsheets function
    """
    gc = GoogleClient().gc

    if not gc:
        return

    try:
        spreadsheets_config = get_spreadsheets_config(gc)
        expenses_config = get_expenses_config(gc)

        total, expenses_data = get_processed_expenses_data(spreadsheets_config, expenses_config, gc)
    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        log_error(error)
        return

    if not total:
        return

    update_google_spreadsheets(expenses_data, gc)
