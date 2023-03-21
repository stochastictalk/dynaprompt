from multiprocessing.managers import ValueProxy
from multiprocessing.synchronize import Event
import os
from time import sleep
from typing import Callable

from colorama import init, Back, Style


def format_role_string(role: str):
    if role == "user":
        return Back.GREEN + f"{role}" + Style.RESET_ALL + "\n"
    elif role == "system":
        return Back.WHITE + f"{role}" + Style.RESET_ALL + "\n"
    elif role == "assistant":
        return Back.MAGENTA + f"{role}" + Style.RESET_ALL + "\n"
    elif role == "error":
        return Back.RED + f"{role}" + Style.RESET_ALL + "\n"
    elif role == "dynaprompt":
        return Back.CYAN + f"{role}" + Style.RESET_ALL + "\n"
    elif role == "conversation_manager":
        return Back.WHITE + f"{role}" + Style.RESET_ALL + "\n"
    else:
        return role


class CLIOutput:
    def __call__(self, message_log_proxy: ValueProxy, stop_event: Event):
        print(">>> CLIOutput launched")
        init()
        id_of_most_recent_message_at_last_render = None
        while not stop_event.is_set():
            sleep(0.1)
            try:
                id_of_last_message_in_log = message_log_proxy.value[-1]["id"]
                if id_of_last_message_in_log != id_of_most_recent_message_at_last_render:
                    os.system("clear")
                    for entry in message_log_proxy.value:
                        print(format_role_string(entry["role"]) + entry["content"])
                    id_of_most_recent_message_at_last_render = id_of_last_message_in_log
            except IndexError:
                pass
