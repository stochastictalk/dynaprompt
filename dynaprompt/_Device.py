from abc import ABC, abstractmethod
from datetime import datetime
import json
from time import sleep

from dynaprompt._get_database_sessionmaker import _get_database_sessionmaker
from dynaprompt._RawMessage import RawMessage
from dynaprompt._Message import Message


class Device(ABC):
    """Base class for devices that get attached to the conversation.

    Database contains message log. Devices consume and emit messages.
    """

    def __init__(
        self,
        database_id="example",
        poll_period=1 # second
        ):
        self._Session = _get_database_sessionmaker(database_id) # Session maker.
        self._poll_period = poll_period
        self._timestamp_of_last_poll = datetime(1970, 1, 1, 0, 0, 0)

    def __call__(
        self
        ): # Perpetually yields messages, processes them with self.process,
        # then writes the response to them into the database's message table.
        # Next step: implement one of these concretely, add watcher.
        while True:
            for input_message in self.get_new_messages():
                response_message = self.process_message(input_message) # Returns None if no response message.
                if response_message is not None:
                    with self._Session() as session:
                        session.add(
                            RawMessage(
                                id=hash(response_message),
                                message=json.dumps(response_message._asdict()),
                                timestamp=datetime.now()
                            )
                        )
                        session.commit()
            sleep(0.1)

    def get_new_messages(self):
        new_timestamp_of_last_poll = datetime.now()
        with self._Session() as session:
            new_raw_messages = session.query(RawMessage).filter(
                RawMessage.timestamp > self._timestamp_of_last_poll
            ).all()
        for raw_message in new_raw_messages:
            yield Message(**json.loads(raw_message.message))
        self._timestamp_of_last_poll = new_timestamp_of_last_poll

    @abstractmethod
    def process_message(
        self,
        input_message: Message
    ) -> Message:
        ...