import logging


logger = logging.getLogger('record.bookings')

def log_error(error):
    logger.error('\nЧто-то не так!')
    logger.error(error)
