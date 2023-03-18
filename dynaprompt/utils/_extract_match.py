import re
from typing import Union

def extract_match(pattern: re.Pattern, text: str) -> Union[str, None]:
    match = pattern.match(text)
    if match:
        return match.group()
    else:
        return None