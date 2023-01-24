from PyQt6.QtCore import QThread, pyqtSignal

from clients.google_client import GoogleClient
from utils.process_expensess_data import get_expenses_data, process_expenses_data
from workers.exprenses.configuration import get_config_spreadsheet
from workers.exprenses.record_expenses import update_google_spreadsheets


class ExpenseWorker(QThread):
    """Thread to execute recording of expenses to Google spreadsheets."""
    log = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ExpenseWorker, self).__init__(parent)

    def run(self):
        gc = GoogleClient().gc
        config = get_config_spreadsheet(gc)

        dataframe = get_expenses_data(gc)
        expenses_data = process_expenses_data(dataframe, config)
        # update_google_spreadsheets(expenses_data)
