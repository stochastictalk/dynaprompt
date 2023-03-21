from dynaprompt import Conversation
from dynaprompt.inputs import CLIInput, DynaPrompt
from dynaprompt.outputs import CLIOutput

if __name__ == "__main__":
    conversation = Conversation(iocallables=[CLIOutput(), DynaPrompt()], main_iocallable=CLIInput())
    conversation()
