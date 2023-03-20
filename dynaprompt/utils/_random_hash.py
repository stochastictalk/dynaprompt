from random import randint
from sys import maxsize

from ._time_since_epoch_ms import _time_since_epoch_ms


def random_hash(optional_string: str = ""):
    return hash(optional_string + str(_time_since_epoch_ms()) + str(randint(0, maxsize)))
