from multiprocessing.managers import ValueProxy
from multiprocessing.synchronize import Event
from time import sleep
from typing import Callable

from dynaprompt.utils import random_hash


class CLIInput:
    def __call__(self, message_log_proxy: ValueProxy, stop_event: Event):
        id_of_last_message_in_log_at_last_input_request = None
        while True:
            sleep(0.1)
            try:
                id_of_last_message_in_log = message_log_proxy.value[-1]["id"]
                if id_of_last_message_in_log_at_last_input_request != id_of_last_message_in_log:
                    id_of_last_message_in_log_at_last_input_request = id_of_last_message_in_log
                    message = input()
                    message_log_proxy.value = message_log_proxy.value + [
                        {"role": "user", "content": message, "id": random_hash()}
                    ]
            except IndexError:
                pass
