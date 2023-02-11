import logging

import pygsheets
from google.auth.exceptions import RefreshError
from pygsheets import AuthenticationError

from clients.http_client import make_custom_http
from constants import SERVICE_ACCOUNT_SECRET_PATH


logger = logging.getLogger('record.bookings')


class GoogleClient:
    def __init__(self):
        self.gc = None

        try:
            self.gc = pygsheets.authorize(service_account_file=SERVICE_ACCOUNT_SECRET_PATH, http=make_custom_http())
            logger.info('Google API client: authorized.')
        except (RefreshError, AuthenticationError) as error:
            logger.error('Google API authorization failed.')
            logger.error(error)
            raise

