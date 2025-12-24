import logging
import sys

def setup_logger(name='mechanical_ai', level=logging.INFO):
    """Sets up a logger for the application."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding multiple handlers if called multiple times
    if not logger.handlers:
        logger.addHandler(ch)

    return logger

# Example usage:
# logger = setup_logger()
# logger.info('This is an informational message.')
