from PyQt6.QtCore import QThread, pyqtSignal

from clients.bnova_client import BnovaClient
from utils.process_bookings_data import process_bookings_data
from workers.bookings.record_bookings import update_google_spreadsheets


class BookingWorker(QThread):
    """Thread to execute recording of bookings to Google spreadsheets."""
    log = pyqtSignal(str)

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
        raw_data = self.bnova_client.get_bookings_data(self.arrival_from, self.arrival_to)
        bookings_data = process_bookings_data(raw_data)

        update_google_spreadsheets(bookings_data)
