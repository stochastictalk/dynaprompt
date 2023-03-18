from typing import NamedTuple

from ._DynaPromptCommandMode import DynaPromptCommandMode

class DynaPromptCommand(NamedTuple):
    recipient: str
    time_prompt: str
    prompt: str
    mode: DynaPromptCommandMode
    incomplete: bool