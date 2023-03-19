from multiprocessing import Manager, Process
from multiprocessing.managers import ValueProxy
import os
from random import randint
from sys import maxsize
from time import time, sleep
from typing import List, Dict

from colorama import init, Fore, Back, Style
from dotenv import dotenv_values
import openai
from dynaprompt import DynaPrompt

# Save your API kay to a .env file with the the entry OPENAI_API_KEY="<your API key>".
config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]


def generate_hash(optional_string: str = ""):
    return hash(optional_string + str(time_since_epoch_ms()) + str(randint(0, maxsize)))

def time_since_epoch_ms():
    return int(time() * 1000)



def receive_user_input(message_log_proxy: ValueProxy):
    id_of_last_message_in_log_at_last_input_request = None
    while True:
        sleep(0.1)
        id_of_last_message_in_log = message_log_proxy.value[-1]["id"]

        # Open a new input each time the log printout updates.
        if id_of_last_message_in_log_at_last_input_request != id_of_last_message_in_log:
            id_of_last_message_in_log_at_last_input_request = id_of_last_message_in_log
            message = input() 
            message_log_proxy.value = message_log_proxy.value + [
                {
                    "role": "user", 
                    "content": message, 
                    "id": generate_hash("user")
                }
            ]


def format_role_string(role: str):
    if role == "user":
        return Back.GREEN + f"{role}" + Style.RESET_ALL + "\n"
    elif role == "system":
        return Back.WHITE + f"{role}" + Style.RESET_ALL + "\n"
    elif role == "assistant":
        return Back.MAGENTA + f"{role}" + Style.RESET_ALL + "\n"
    else:
        return role


def render_log(message_log_proxy: ValueProxy):
    try:
        id_of_most_recent_message_at_last_render = None
        while True:
            sleep(0.05)
            id_of_last_message_in_log = message_log_proxy.value[-1]["id"]
            if id_of_last_message_in_log != id_of_most_recent_message_at_last_render:
                os.system("clear")
                for entry in message_log_proxy.value:
                    print(format_role_string(entry["role"]) + entry['content'])
                id_of_most_recent_message_at_last_render = id_of_last_message_in_log
    except KeyboardInterrupt:
        pass


def remove_ids(message_log: List[Dict]):
    # @TODO come up with a less shitty way to manage ids
    return [{i:d[i] for i in d if i != "id"} for d in message_log]

def receive_chatbot_input(message_log_proxy: ValueProxy):
    # Needs to listen for new inputs.
    # Has view of current state of message_log_proxy. State changes.
    # Make new request if latest message was not the one just sent.
    try:
        id_of_last_message_chatbot_sent = None
        while True:
            sleep(0.1)
            id_of_last_message_in_log = message_log_proxy.value[-1]["id"]
            if id_of_last_message_in_log != id_of_last_message_chatbot_sent:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=remove_ids(message_log_proxy.value)
                ) # @TODO Handle API request failure.
                message = response["choices"][0]["message"]["content"]
                id_of_last_message_chatbot_sent = generate_hash("assistant")
                message_log_proxy.value = message_log_proxy.value + [
                    {"role": "assistant", "content": message, "id": id_of_last_message_chatbot_sent}
                ]
    except KeyboardInterrupt:
        pass


def openai_chat_completion():
    init() # Initialize colorama.
    try:
        manager = Manager() # Used to share state between processes.
        message_log_proxy = manager.Value(
            "message_log_proxy", 
            [{
                "role": "system",
                "content": "You are a helpful, wise-cracking assistant named PLEX.",
                "id": generate_hash("system")
            }]
        )
        chatbot_process = Process(target=receive_chatbot_input, args=(message_log_proxy,))
        render_process = Process(target=render_log, args=(message_log_proxy,))
        processes = [chatbot_process, render_process]

        for p in processes: 
            p.start()

        receive_user_input(message_log_proxy) # Blocking, must be run in main process.

    except KeyboardInterrupt:
        for p in processes:
            p.join()

#dp = DynaPrompt()