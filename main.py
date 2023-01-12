import logging

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog, QApplication, QVBoxLayout, QPushButton, QLabel, QWidget, QFormLayout, QPlainTextEdit, QTextEdit, )

import sys

from record_bookings import record_bookings


logger = logging.getLogger('record.bookings')
logging.basicConfig()
logger.setLevel(logging.DEBUG)
# consoleHandler = logging.StreamHandler()
# logger.addHandler(consoleHandler)


class BookingWorker(QThread):
    """Thread to execute bookings recording."""
    log = pyqtSignal(str)

    def __init__(self, parent=None):
        super(BookingWorker, self).__init__(parent)
        self.filename = None

    def set_file(self, filename):
        if not self.isRunning():
            self.filename = filename

    def run(self):
        record_bookings(self.filename)

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

        self.booking_worker = BookingWorker(self)
        # self.expense_worker = ExpenseWorker(self)

        self.filename = QLabel('/Users/marina.korniychuk/Downloads/19057_bookings_20230107031414_1.xlsx')

        self.btnSelect = QPushButton('Select file')
        self.btnSelect.clicked.connect(self.get_file)

        self.btnStartWorker = QPushButton('Start Worker')
        self.btnStartWorker.clicked.connect(self.start_booking_worker)

        self.logTextBox = QTextEditLogger(self)
        self.configure_app_logger()

        self.formLayout = QFormLayout()
        self.set_app_layout()
        layout.addLayout(self.formLayout)

        self.setGeometry(300, 300, 550, 450)
        self.setLayout(layout)
        self.setWindowTitle("Bookings")


    def set_app_layout(self):
        self.formLayout.addRow(QLabel('Record bookings from:'))
        self.formLayout.addRow('File:', self.filename)
        self.formLayout.addRow(self.btnSelect)
        self.formLayout.addRow(self.btnStartWorker)
        self.formLayout.addRow(self.logTextBox.widget)
    def configure_app_logger(self):
        self.logTextBox.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(self.logTextBox)
        logger.setLevel(logging.DEBUG)

    def start_booking_worker(self):
        if not self.booking_worker.isRunning():
            self.booking_worker.set_file(self.filename.text())
            self.booking_worker.start()

    # def start_expense_worker(self):
    #     if not self.booking_worker.isRunning():
    #         self.booking_worker.start()

    def get_file(self):
        fname = QFileDialog.getOpenFileName(
            self,
            'Open file',
            '/Users/marina.korniychuk/Downloads', "Excel Files (*.xls *.xml *.xlsx *.xlsm)"
        )
        self.filename.setText(fname[0])

    def record_bookings(self):
        record_bookings(self.filename.text())

def main():
    app = QApplication(sys.argv)
    ex = BookingsWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

