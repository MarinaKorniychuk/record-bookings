import logging

from PyQt6.QtWidgets import (
    QFileDialog, QApplication, QVBoxLayout, QPushButton, QLabel, QWidget, QFormLayout, QPlainTextEdit, )

import sys

from record_bookings import record_bookings


logger = logging.getLogger('record.bookings')
logger.setLevel(logging.DEBUG)
# consoleHandler = logging.StreamHandler()
# logger.addHandler(consoleHandler)

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

        layout = QVBoxLayout()

        self.filename = QLabel('/Users/marina.korniychuk/Downloads/19057_bookings_20230107031414_1.xlsx')

        self.btnSelect = QPushButton('Select file')
        self.btnSelect.clicked.connect(self.getfile)

        self.btnStart = QPushButton('Start')
        self.btnStart.clicked.connect(self.test)

        formLayout = QFormLayout()
        formLayout.addRow(QLabel('Record bookings from:'))
        formLayout.addRow('File:', self.filename)
        formLayout.addRow(self.btnSelect)
        formLayout.addRow(self.btnStart)

        logTextBox = QTextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        logger.addHandler(logTextBox)
        logger.setLevel(logging.DEBUG)

        # self._button = QPushButton(self)
        # self._button.setText('Test Me')

        # Add the new logging box widget to the layout
        formLayout.addRow(logTextBox.widget)
        # layout.addWidget(self._button)
        # self.setLayout(layout)

        # Connect signal to slot
        # self._button.clicked.connect(self.test)

        layout.addLayout(formLayout)

        self.setGeometry(300, 300, 550, 450)
        self.setLayout(layout)
        self.setWindowTitle("Bookings")

    def test(self):
        # logger = logging.getLogger('record.bookings')
        logger.debug('damn, a bug')
        logger.info('something to remember')
        logging.warning('that\'s not right')
        logging.error('foobar')

        self.record_bookings()

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

