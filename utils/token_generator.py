import random
import time
from utils import MD5_helper


class TokenGenerator():
    @classmethod
    def generate(cls):
        source = int(time.time())
        source += random.randint(500,1000)**3
        result = MD5_helper.MD5Helper.hash(str(source))
        return result[:5].upper()