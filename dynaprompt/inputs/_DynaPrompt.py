from enum import Enum
import logging
from multiprocessing.managers import ValueProxy
from multiprocessing.synchronize import Event
import re
from time import sleep
from typing import NamedTuple

from dynaprompt.utils import extract_match, random_hash


class DynaPromptCommandMode(Enum):
    SCHEDULE = 0
    DESCHEDULE = 1


class DynaPromptCommand(NamedTuple):
    recipient: str
    time_prompt: str
    prompt: str
    mode: DynaPromptCommandMode
    incomplete: bool


class DynaPrompt:
    def __init__(self):
        self.role = "dynaprompt"
        self._regexps = {
            "dps_command": re.compile(r"^\s*dps"),
            "dpd_command": re.compile(r"^\s*dpd"),
            "recipient": re.compile(r"\S+\s+(\S+)"),
            "time_prompt": re.compile(r"\b\w+\s+\w+\s+([^\n]+)"),
            "prompt": re.compile(r"[^\n]+\n(.*)", flags=re.DOTALL),
        }
        self.schedule = []

    def __call__(self, message_log_proxy: ValueProxy, stop_event: Event):

        # Include start-up message.
        id_of_most_recently_processed_message = random_hash()
        message_log_proxy.value = message_log_proxy.value + [
            {"role": self.role, "content": "dynaprompt initialized.", "id": id_of_most_recently_processed_message}
        ]

        while not stop_event.is_set():
            try:
                last_message_in_log = message_log_proxy.value[-1]
                if id_of_most_recently_processed_message != last_message_in_log["id"]:
                    message_id = self._process_message(last_message_in_log["content"], message_log_proxy)
                    id_of_most_recently_processed_message = message_id
            except IndexError:
                pass
            sleep(0.1)

    def _process_message(self, message: str, message_log_proxy: ValueProxy):
        """Processes a message.

        Parameters
        ----------
        message : str
            Message to be processed.

        Returns
        -------
            None
        """
        message_id = random_hash()

        # Route raw message to appropriate command.
        if self._regexps["dps_command"].match(message):
            command = self._extract_command(mode=DynaPromptCommandMode.SCHEDULE, message=message)
            self._schedule(command, message_log_proxy, message_id)
        elif self._regexps["dpd_command"].match(message):
            command = self._extract_command(mode=DynaPromptCommandMode.DESCHEDULE, message=message)
            self._deschedule(command, message_log_proxy, message_id)
        else:
            self._ignore(message_log_proxy, message_id)

        return message_id

    def _schedule(self, command: DynaPromptCommand, message_log_proxy: ValueProxy, message_id: str):
        self.schedule.append(command)
        message_log_proxy.value = message_log_proxy.value + [
            {"role": "dynaprompt", "content": f"{command}", "id": message_id}
        ]

    def _deschedule(self, command: DynaPromptCommand, message_log_proxy: ValueProxy, message_id: str):
        self.schedule.append(command)
        message_log_proxy.value = message_log_proxy.value + [
            {"role": "dynaprompt", "content": f"{command}", "id": message_id}
        ]

    def _ignore(self, message_log_proxy: ValueProxy, message_id: str):
        message_log_proxy.value = message_log_proxy.value + [
            {"role": "dynaprompt", "content": "message ignored", "id": message_id}
        ]

    def _extract_command(self, mode: DynaPromptCommandMode, message: str) -> DynaPromptCommand:
        """Maps raw command message to structured format."""
        recipient = extract_match(self._regexps["recipient"], message)
        time_prompt = extract_match(self._regexps["time_prompt"], message)
        prompt = extract_match(self._regexps["prompt"], message)
        if mode == DynaPromptCommandMode.SCHEDULE:
            return DynaPromptCommand(
                mode=mode,
                recipient=recipient,
                time_prompt=time_prompt,
                prompt=prompt,
                incomplete=((recipient is None) or (time_prompt is None) or (prompt is None)),
            )
        elif mode == DynaPromptCommandMode.DESCHEDULE:
            return DynaPromptCommand(
                mode=mode,
                recipient=recipient,
                time_prompt=time_prompt,
                prompt=prompt,
                incomplete=((recipient is None) or (time_prompt is None) or (prompt is None)),
            )
        else:
            raise ValueError("'mode' should be a DynaPromptCommandMode")
