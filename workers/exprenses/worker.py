from PyQt6.QtCore import QThread, pyqtSignal

from clients.google_client import GoogleClient
from utils.process_expensess_data import get_expenses_data, process_expenses_data
from utils.configuration import get_expenses_config, get_spreadsheets_config, get_form_responses_spreadsheet_data
from workers.exprenses.record_expenses import update_google_spreadsheets


class ExpenseWorker(QThread):
    """Thread to execute recording of expenses to Google spreadsheets."""
    log = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ExpenseWorker, self).__init__(parent)

    def run(self):
        gc = GoogleClient().gc

        spreadsheets_config = get_spreadsheets_config(gc)
        expenses_config = get_expenses_config(gc)
        form_responses_spreadsheet_data = get_form_responses_spreadsheet_data(gc)

        dataframe = get_expenses_data(form_responses_spreadsheet_data, gc)
        # expenses_data = process_expenses_data(dataframe, spreadsheets_config, expenses_config)
        # update_google_spreadsheets(expenses_data)
