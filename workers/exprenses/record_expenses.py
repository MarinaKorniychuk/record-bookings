import logging
from datetime import datetime

import httplib2
import pygsheets

logger = logging.getLogger('record.bookings')


def record_expenses_to_spreadsheet(spreadsheet, records, skipped):
    pass

def update_google_spreadsheets(data, gc):
    """Transfer records from dataset to Google spreadsheets"""
    logger.info(f'Started recording data at {datetime.now().time()}\n')

    skipped = []
    # recording is done for each spreadsheet one by one as they are specified in data
    for spreadsheet_id, records in data.items():
        try:
            # open spreadsheet by its id (ids stored in constants.py file)
            spreadsheet = gc.open_by_key(spreadsheet_id)
            record_expenses_to_spreadsheet(spreadsheet, records, skipped)
        except pygsheets.SpreadsheetNotFound:
            logger.warning(f'{spreadsheet_id} spreadsheet not found, skip.')
            pass
        except httplib2.HttpLib2Error as error:
            logger.error(f'Could not open {spreadsheet_id} spreadsheet: {error}')

    logger.info(f'Finished recording data at {datetime.now().time()}\n')

    logger.info(f'SKIPPED RECORDS: \n{skipped}')


# d[d.recorded.notnull()]
# d['recorded'] = d['recorded'].fillna(0)
# not_recordered = d[d.recorded.isin([0.0])]
# d[d.recorded == 0.0]

# int(an.value or 0) + 4
# cell.note = note
# empty note in None