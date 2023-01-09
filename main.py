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


class Thread(QThread):
    log = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self.filename = None

    def setFile(self, filename):
        if not self.isRunning():
            self.filename = filename

    def run(self):
        record_bookings(self.filename)

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class BookingsWindow(QWidget):
    def __init__(self, parent=None):
        super(BookingsWindow, self).__init__(parent)

        self._worker = Thread(self)

        layout = QVBoxLayout()

        self.filename = QLabel('/Users/marina.korniychuk/Downloads/19057_bookings_20230107031414_1.xlsx')

        self.btnSelect = QPushButton('Select file')
        self.btnSelect.clicked.connect(self.getfile)

        self.btnStartWorker = QPushButton('Start Worker')
        self.btnStartWorker.clicked.connect(self.start_worker)

        formLayout = QFormLayout()
        formLayout.addRow(QLabel('Record bookings from:'))
        formLayout.addRow('File:', self.filename)
        formLayout.addRow(self.btnSelect)
        formLayout.addRow(self.btnStartWorker)

        logTextBox = QTextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter('%(message)s'))

        logger.addHandler(logTextBox)
        logger.setLevel(logging.DEBUG)

        formLayout.addRow(logTextBox.widget)

        layout.addLayout(formLayout)

        self.setGeometry(300, 300, 550, 450)
        self.setLayout(layout)
        self.setWindowTitle("Bookings")

    def process(self):
        self._worker.setFile(self.filename.text())
        self._worker.start()

    def start_worker(self):
        if not self._worker.isRunning():
            self.process()

    def getfile(self):
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

