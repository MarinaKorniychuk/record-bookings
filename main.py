import datetime
import logging
import sys

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QPushButton, QLabel, QWidget, QFormLayout, QPlainTextEdit)

from workers.booking_worker import BookingWorker

logger = logging.getLogger('record.bookings')
logging.basicConfig()
logger.setLevel(logging.DEBUG)
# consoleHandler = logging.StreamHandler()
# logger.addHandler(consoleHandler)


class QTextEditLogger(logging.Handler):
    """Customized handler to output logs in text widget in real-time."""
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
        self.widget.centerCursor()  # scroll to the bottom


class BookingsWindow(QWidget):
    def __init__(self, parent=None):
        super(BookingsWindow, self).__init__(parent)

        layout = QVBoxLayout()

        self.arrival_from_date = QtWidgets.QDateEdit(calendarPopup=True)
        self.arrival_from_date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.arrival_to_date = QtWidgets.QDateEdit(calendarPopup=True)
        self.arrival_to_date.setDateTime(QtCore.QDateTime.currentDateTime())

        self.booking_worker = BookingWorker(self)
        # self.expense_worker = ExpenseWorker(self)

        self.btnStartBookingWorker = QPushButton('Заполнить приходы')
        self.btnStartBookingWorker.clicked.connect(self.start_booking_worker)

        self.logTextBox = QTextEditLogger(self)
        self.configure_app_logger()

        self.formLayout = QFormLayout()
        self.set_app_layout()
        layout.addLayout(self.formLayout)

        self.setGeometry(300, 300, 550, 450)
        self.setLayout(layout)
        self.setWindowTitle("Bookings")

    def set_app_layout(self):
        self.formLayout.addRow(QLabel('Выберите период для получения бронирований с Bnova'))
        self.formLayout.addRow(QLabel('Дата заезда: '), self.arrival_from_date)
        self.formLayout.addRow(QLabel('по '), self.arrival_to_date)
        self.formLayout.addRow(self.btnStartBookingWorker)

        self.formLayout.addRow(self.logTextBox.widget)

    def configure_app_logger(self):
        self.logTextBox.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(self.logTextBox)
        logger.setLevel(logging.DEBUG)

    def start_booking_worker(self):
        arrival_from = datetime.date(*self.arrival_from_date.date().getDate())
        arrival_to = datetime.date(*self.arrival_to_date.date().getDate())

        if not self.booking_worker.isRunning():
            self.booking_worker.set_dates(arrival_from, arrival_to)
            self.booking_worker.start()

    # def start_expense_worker(self):
    #     if not self.booking_worker.isRunning():
    #         self.booking_worker.start()


def main():
    app = QApplication(sys.argv)
    ex = BookingsWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

