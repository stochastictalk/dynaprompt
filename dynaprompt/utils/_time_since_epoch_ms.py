from time import time


def _time_since_epoch_ms():
    return int(time() * 1000)
