import re
from typing import Union


def extract_match(pattern: re.Pattern, text: str) -> Union[str, None]:
    match = pattern.match(text)
    if match:
        try:
            return match.group(1)
        except:
            return match.group(0)
    else:
        return None