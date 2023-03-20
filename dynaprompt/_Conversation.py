from multiprocessing import Manager, Process
from multiprocessing.managers import ValueProxy
from multiprocessing.synchronize import Event
from time import sleep
from typing import Callable, List, Union


class Conversation:
    def __init__(
        self,
        iocallables: Callable[[ValueProxy, Event], None],
        main_iocallable: Union[Callable[[ValueProxy, Event], None], None] = None,
    ):
        self.iocallables = iocallables
        self.main_iocallable = main_iocallable

    # @TODO: include reading and writing log to disk.

    def __call__(self):
        manager = Manager()  # Used to share state between processes.
        message_log_proxy = manager.Value("message_log_proxy", [])
        stop_event = manager.Event()
        processes = [Process(target=f, args=(message_log_proxy, stop_event)) for f in self.iocallables]

        for p in processes:
            p.start()

        try:
            if self.main_iocallable is not None:
                self.main_iocallable(message_log_proxy, stop_event)
            else:
                while True:
                    sleep(10)  # Intentionally empty.
        except KeyboardInterrupt:
            stop_event.set()
            p.join()
