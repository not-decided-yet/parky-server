import logging
import sys


def get_logger():
    """
    Generate logger.
    """
    logger = logging.getLogger("ParkyVehicle")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
    logger.addHandler(stream_handler)
    return logger
