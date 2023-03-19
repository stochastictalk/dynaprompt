from dynaprompt import DynaPrompt
from dynaprompt import DynaPromptCommand
from dynaprompt import DynaPromptCommandMode


def _extract_command_1(dp: DynaPrompt):
    message = "dps user tomorrow afternoon\nsome bullshit"
    command = dp._extract_command(DynaPromptCommandMode.SCHEDULE, message)
    assert command.recipient == "user"
    assert command.time_prompt == "tomorrow afternoon"
    assert command.prompt == "some bullshit"

def _extract_command_2(dp: DynaPrompt):
    message = "dps user tomorrow afternoon\nsome bullshit\nsome more bullshit"
    command = dp._extract_command(DynaPromptCommandMode.SCHEDULE, message)
    assert command.recipient == "user"
    assert command.time_prompt == "tomorrow afternoon"
    assert command.prompt == "some bullshit\nsome more bullshit"

def _extract_command_3(dp: DynaPrompt):
    message = "dps user tomorrow afternoon\n"
    command = dp._extract_command(DynaPromptCommandMode.SCHEDULE, message)
    assert command.recipient == "user"
    assert command.time_prompt == "tomorrow afternoon"
    assert command.prompt == ""

def _extract_command_4(dp: DynaPrompt):
    message = "dps unknown tomorrow afternoon\n"
    command = dp._extract_command(DynaPromptCommandMode.SCHEDULE, message)
    assert command.recipient == "unknown"
    assert command.time_prompt == "tomorrow afternoon"
    assert command.prompt == ""

def _extract_command_5(dp: DynaPrompt):
    message = "dps"
    command = dp._extract_command(DynaPromptCommandMode.SCHEDULE, message)
    assert command.recipient == None
    assert command.time_prompt == None
    assert command.prompt == None

def _extract_command_6(dp: DynaPrompt):
    message = "dps user"
    command = dp._extract_command(DynaPromptCommandMode.SCHEDULE, message)
    assert command.recipient == "user"
    assert command.time_prompt == None
    assert command.prompt == None

def _extract_command_7(dp: DynaPrompt):
    message = "dps user 1679221003"
    command = dp._extract_command(DynaPromptCommandMode.SCHEDULE, message)
    assert command.recipient == "user"
    assert command.time_prompt == "1679221003"
    assert command.prompt == None

def test_DynaPrompt():
    dp = DynaPrompt()
    _extract_command_1(dp)
    _extract_command_2(dp)
    _extract_command_3(dp)
    _extract_command_4(dp)
    _extract_command_5(dp)
    _extract_command_6(dp)
    _extract_command_7(dp)

    
    