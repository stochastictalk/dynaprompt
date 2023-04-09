from dynaprompt import Device, Message

class CLIInput(Device):
    
    def process_message(self, input_message: Message):
        message_text = input()
        return Message(
            device_id="user",
            content=message_text
        )
