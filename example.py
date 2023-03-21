from dynaprompt import Conversation
from dynaprompt.inputs import CLIInput, OpenAIChat
from dynaprompt.outputs import CLIOutput

if __name__ == "__main__":
    conversation = Conversation(iocallables=[CLIOutput(), OpenAIChat()], main_iocallable=CLIInput())
    conversation()
