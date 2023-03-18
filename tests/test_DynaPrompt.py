from dynaprompt import DynaPrompt
from dynaprompt import DynaPromptCommand
from dynaprompt import DynaPromptCommandMode


def _extract_command_one(dp: DynaPrompt):
    message = "dps user tomorrow afternoon\nsome bullshit"
    
    command = dp._extract_command(DynaPromptCommandMode.SCHEDULE, message)
    assert command.recipient == "user"
    assert command.time_prompt == "tomorrow afternoon"
    assert command.prompt == "some bullshit"


def test_DynaPrompt():
    dp = DynaPrompt()
    _extract_command_one(dp)

    
    