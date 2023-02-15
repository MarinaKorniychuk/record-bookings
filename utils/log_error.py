import logging


logger = logging.getLogger('record.bookings')

def log_error(error):
    logger.error('SOMETHING WENT WRONG!')
    logger.error(error)
