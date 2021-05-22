import logging
import random
import string
import sys


def get_logger(name: str = "ParkyVehicle"):
    """
    Generate logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
    logger.addHandler(stream_handler)
    return logger


def generate_random_token(length: int):
    """Generate random token by given length."""
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


class Singleton:
    """
    Class for applying singleton pattern.
    """

    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls.__get_instance
        return cls.__instance
