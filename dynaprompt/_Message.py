from datetime import datetime
from typing import NamedTuple

class Message(NamedTuple):
    device_id: str
    content: str