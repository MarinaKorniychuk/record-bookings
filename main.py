import datetime
import logging
import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QPushButton, QLabel, QWidget, QFormLayout, QDateEdit
                             )
from bookings.record_bookings import run as record_bookings
from exprenses.record_expenses import run as record_expenses

logger = logging.getLogger('record.bookings')
logging.basicConfig(format='%(message)s')
logger.setLevel(logging.INFO)


class BookingsWindow(QWidget):
    def __init__(self, parent=None):
        super(BookingsWindow, self).__init__(parent)

        layout = QVBoxLayout()

        self.arrival_from_date = QDateEdit(calendarPopup=True)
        self.arrival_from_date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.arrival_to_date = QDateEdit(calendarPopup=True)
        self.arrival_to_date.setDateTime(QtCore.QDateTime.currentDateTime())

        self.btnStartBookingWorker = QPushButton('Заполнить приходы')
        self.btnStartBookingWorker.clicked.connect(self.start_recording_bookings)

        self.btnStartExpenseWorker = QPushButton('Заполнить расходы')
        self.btnStartExpenseWorker.clicked.connect(self.start_recording_expenses)

        self.formLayout = QFormLayout()
        self.set_app_layout()
        layout.addLayout(self.formLayout)

        self.setGeometry(300, 300, 550, 270)
        self.setLayout(layout)
        self.setWindowTitle("Bookings")

    def set_app_layout(self):
        self.formLayout.addRow(QLabel('Выберите период для получения бронирований с Bnova'))
        self.formLayout.addRow(QLabel('Дата заезда: '), self.arrival_from_date)
        self.formLayout.addRow(QLabel('по '), self.arrival_to_date)
        self.formLayout.addRow(self.btnStartBookingWorker)
        self.formLayout.addRow(QLabel(''))
        self.formLayout.addRow(QLabel('Нажмите, чтобы внести в таблицу все новые расходы: '))
        self.formLayout.addRow(self.btnStartExpenseWorker)

    def start_recording_bookings(self):
        arrival_from = datetime.date(*self.arrival_from_date.date().getDate()).strftime('%d.%m.%Y')
        arrival_to = datetime.date(*self.arrival_to_date.date().getDate()).strftime('%d.%m.%Y')

        record_bookings(arrival_from, arrival_to)

    def start_recording_expenses(self):
        record_expenses()


def main():
    app = QApplication(sys.argv)
    ex = BookingsWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

