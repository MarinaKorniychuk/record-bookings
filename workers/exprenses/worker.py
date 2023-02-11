from PyQt6.QtCore import QThread
from pygsheets import SpreadsheetNotFound, WorksheetNotFound

from clients.google_client import GoogleClient
from utils.log_error import log_error
from utils.process_expensess_data import get_processed_expenses_data
from utils.configuration import get_expenses_config, get_spreadsheets_config
from workers.exprenses.record_expenses import update_google_spreadsheets


class ExpenseWorker(QThread):
    """Thread to execute recording of expenses to Google spreadsheets."""
    # log = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ExpenseWorker, self).__init__(parent)

    def run(self):
        gc = GoogleClient().gc

        if not gc:
            return

        try:
            spreadsheets_config = get_spreadsheets_config(gc)
            expenses_config = get_expenses_config(gc)

            expenses_data = get_processed_expenses_data(spreadsheets_config, expenses_config, gc)
        except (SpreadsheetNotFound, WorksheetNotFound) as error:
            log_error(error)
            return

        update_google_spreadsheets(expenses_data, gc)
