from enum import Enum
import logging
import re

from .utils import extract_match
from ._DynaPromptCommand import DynaPromptCommand
from ._DynaPromptCommandMode import DynaPromptCommandMode

class DynaPrompt:

    def __init__(self):
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._logger.info("initialized")
        self._regexps = {
            "dps_command": re.compile(r"^\s*dps"),
            "dpd_command": re.compile(r"^\s*dpd"),
            "recipient": re.compile(r"\S+\s+(\S+)"),
            "time_prompt": re.compile(r"\b\w+\s+\w+\s+([^\n]+)"),
            "prompt": re.compile(r"[^\n]+\n(.*)", flags=re.DOTALL)
        }
        self.schedule = dict()

    def __call__(self, message: str):
        """Processes a message.
        """
        # Route raw message to appropriate command.
        if self._regexps["dps_command"].match(message):
            self._logger("recognized command 'dps'")
            command = self._extract_command(mode=DynaPromptCommandMode.SCHEDULE, message=message)
            return self._schedule(command)
        elif self._regexps["dpd_command"].match(message):
            self._logger("recognized command 'dpd'")
            command = self._extract_command(mode=DynaPromptCommandMode.DESCHEDULE, message=message)
            return self._deschedule(command)
        else: 
            self._logger("no command recognized")
            return self._ignore(command)

    def _schedule(self, command: DynaPromptCommand):
        self.schedule.append(command)

    def _deschedule(self, command: DynaPromptCommand):
        self.schedule.append(command)

    def _extract_command(self, mode: DynaPromptCommandMode, message: str):
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
                incomplete=((recipient is None) or (time_prompt is None) or (prompt is None))
            )
        elif mode == DynaPromptCommandMode.DESCHEDULE:
            return DynaPromptCommand(
                mode=mode,
                recipient=recipient,
                time_prompt=time_prompt,
                prompt=prompt,
                incomplete=((recipient is None) or (time_prompt is None) or (prompt is None))
            )
        else:
            raise ValueError("'mode' should be a DynaPromptCommandMode")

    
    def _ignore(self, message: str):
        pass