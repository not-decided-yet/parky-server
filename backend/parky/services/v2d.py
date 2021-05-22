import random
import string

from parky.utils import Singleton

def generate_random_token(length: int):
    """Generate random token by given length."""
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

class V2DService(Singleton):
    def __init__(self):
        self.
