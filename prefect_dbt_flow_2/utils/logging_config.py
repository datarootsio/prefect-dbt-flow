import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.setLevel(logging.DEBUG)

# Create a file handler and set the log file path
log_file_path = 'dev_logs.log'
file_handler = logging.FileHandler(log_file_path)

# Create a console handler for printing log messages to the console
console_handler = logging.StreamHandler()

# Define a log format
log_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
file_handler.setFormatter(log_format)
console_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
