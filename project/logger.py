import logging
import os

e_log = logging.getLogger("error")
logger = logging.getLogger("log")
logger.setLevel(logging.INFO)

# Create handlers
abs_path = str(__file__).replace(str(os.path.basename(__file__)), '')
e_handler = logging.FileHandler(abs_path + 'log/Error.log')
log_handler = logging.FileHandler(abs_path + 'log/log.log')
e_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
e_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
e_handler.setFormatter(e_format)
log_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(log_handler)
e_log.addHandler(e_handler)


def error(*args):
    e_log.error(*args)


def log(*args):
    logger.info(*args)
