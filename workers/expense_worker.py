from PyQt6.QtCore import QThread, pyqtSignal

from record_expenses import update_google_spreadsheets


class ExpenseWorker(QThread):
    """Thread to execute recording of expenses to Google spreadsheets."""
    log = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ExpenseWorker, self).__init__(parent)

    def run(self):
        pass
        # raw_data = get_expenses_data()
        # expenses_data = process_expenses_data(raw_data)
        # update_google_spreadsheets(expenses_data)
