import logging

from PyQt6.QtCore import QThread
from pygsheets import SpreadsheetNotFound, WorksheetNotFound

from clients.bnova_client import BnovaClient
from clients.google_client import GoogleClient
from utils.log_error import log_error
from utils.process_bookings_data import process_bookings_data
from utils.configuration import get_bookings_config, get_spreadsheets_config
from workers.bookings.record_bookings import update_google_spreadsheets


logger = logging.getLogger('record.bookings')

class BookingWorker(QThread):
    """Thread to execute recording of bookings to Google spreadsheets."""
    # log = pyqtSignal(str)

    def __init__(self, parent=None):
        super(BookingWorker, self).__init__(parent)
        self.bnova_client = BnovaClient()

        self.arrival_from = None
        self.arrival_to = None

    def set_dates(self, arrival_from, arrival_to):
        if not self.isRunning():
            self.arrival_from = arrival_from.strftime('%d.%m.%Y')
            self.arrival_to = arrival_to.strftime('%d.%m.%Y')

    def run(self):
        gc = GoogleClient().gc

        if not gc:
            return

        try:
            spreadsheets_config = get_spreadsheets_config(gc)
            bookings_config = get_bookings_config(gc)
        except (SpreadsheetNotFound, WorksheetNotFound) as error:
            log_error(error)
            return

        raw_data = self.bnova_client.get_bookings_data(self.arrival_from, self.arrival_to)
        bookings_data = process_bookings_data(raw_data, spreadsheets_config, bookings_config)

        update_google_spreadsheets(bookings_data, gc)
