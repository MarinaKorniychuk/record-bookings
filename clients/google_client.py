import logging

import pygsheets

from clients.http_client import make_custom_http
from constants import CLIENT_SECRET_PATH


logger = logging.getLogger('record.bookings')


class GoogleClient:
    def __init__(self):
        self.gc = pygsheets.authorize(CLIENT_SECRET_PATH, http=make_custom_http())
        logger.info('Google API client: authorized.')

