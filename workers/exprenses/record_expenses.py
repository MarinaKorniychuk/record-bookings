import logging
import time
from datetime import datetime

import httplib2
import pygsheets

from utils.configuration import get_form_responses_worksheet
from utils.date_helper import get_expense_date
from utils.spreadsheet_operations import get_worksheet_name_by_month, open_or_create_worksheet, \
    get_expense_cell_address_by_date, update_expense_cell_value, update_cell_with_value

logger = logging.getLogger('record.bookings')


def record_expenses_to_spreadsheet(spreadsheet, records, response_worksheet, skipped):
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
                f'{record["amount"]} expense for {record["category"]} category from {expense_date} is recorded\n'
            )

            time.sleep(2)

        except httplib2.HttpLib2Error as error:
            logger.error(f'Caught the following error: {error}')

            skipped.append(record)
            continue

    logger.info(f'{spreadsheet.title} IS DONE\n')

def update_google_spreadsheets(data, gc):
    """Transfer records from dataset to Google spreadsheets"""
    logger.info(f'Started recording data at {datetime.now().time()}\n')

    expenses_worksheet = get_form_responses_worksheet(gc)

    skipped = []
    # recording is done for each spreadsheet one by one as they are specified in data
    for spreadsheet_title, records in data.items():
        try:
            # open spreadsheet by its id (ids stored in constants.py file)
            spreadsheet = gc.open(spreadsheet_title)
            record_expenses_to_spreadsheet(spreadsheet, records, expenses_worksheet, skipped)
        except pygsheets.SpreadsheetNotFound:
            logger.warning(f'{spreadsheet_title} spreadsheet not found, skip.')
            skipped.append(records)
        except httplib2.HttpLib2Error as error:
            logger.error(f'Could not open {spreadsheet_title} spreadsheet: {error}')
            skipped.append(records)


    logger.info(f'Finished recording data at {datetime.now().time()}\n')

    logger.info(f'SKIPPED RECORDS: \n{skipped}')


# d[d.recorded.notnull()]
# d['recorded'] = d['recorded'].fillna(0)
# not_recordered = d[d.recorded.isin([0.0])]
# d[d.recorded == 0.0]

# int(an.value or 0) + 4
# cell.note = note
# empty note is None
