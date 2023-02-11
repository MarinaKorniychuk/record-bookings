import logging


logger = logging.getLogger('record.bookings')

def log_error(error: object) -> object:
    logger.error('SOMETHING WENT WRONG!')
    logger.error(error)
