from multiprocessing.managers import ValueProxy
from multiprocessing.synchronize import Event
from time import sleep

class TTSOutput:

    def __call__(
        self,
        message_log_proxy: ValueProxy,
        stop_event: Event,
        role: str = "assistant"
        ):
        print(">>> TTS output launched")
        id_of_most_recent_message_at_last_render = None
        while not stop_event.is_set():
            sleep(0.1)
            try:
                id_of_last_message_in_log = message_log_proxy.value[-1]["id"]
                if id_of_last_message_in_log != id_of_most_recent_message_at_last_render:
                    if id_of_last_message_in_log["user"] == role:
                        
                    id_of_most_recent_message_at_last_render = id_of_last_message_in_log
            except IndexError:
                pass
