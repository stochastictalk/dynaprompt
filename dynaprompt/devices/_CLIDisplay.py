import os

from colorama import init, Back, Style

from dynaprompt import Device, Message



def format_role_string(role: str):
    if role == "user":
        return Back.GREEN + f"{role}" + Style.RESET_ALL + "\n"
    elif role == "database":
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


class CLIDisplay(Device):

    def __init__(self):
        init()
        self.messages = []
        super().__init__()
    
    def process_message(
        self,
        input_message: Message
        ):
        # Gets all messages and displays them.
        self.messages.append(input_message)
        os.system("clear")
        for entry in self.messages:
            print(format_role_string(entry.device_id) + entry.content)
        