import logging
import os


def get_logger(name):
    # Logger instance
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # File handler
    log_file = os.path.join(os.path.dirname(__file__), "bot.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s')

    # Add handlers to the loggers and set the formatter
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    return logger
