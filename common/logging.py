import logging

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logging.getLogger().setLevel(logging.INFO)
    return logger