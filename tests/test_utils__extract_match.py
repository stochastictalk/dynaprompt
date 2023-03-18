import re

def test_utils__extract_match():
    from dynaprompt.utils import extract_match
    assert extract_match(re.compile("hello"), "hello world") == "hello"
    assert extract_match(re.compile("pig"), "hello world") is None