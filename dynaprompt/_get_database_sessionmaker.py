from datetime import datetime
from functools import lru_cache
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dynaprompt._Base import Base
from dynaprompt._RawMessage import RawMessage # Uses 'Base' declarative base.
from dynaprompt._Message import Message

@lru_cache
def _get_database_sessionmaker(database_id="example"):
    # Set up the database URL with the necessary credentials and database name
    db_url = f"sqlite:///{database_id}.db"

    # Create the engine
    engine = create_engine(db_url)

    # Create the table if it doesn't already exist
    Base.metadata.create_all(engine)

    # Create a session maker.
    session_maker = sessionmaker(bind=engine)

    # Add a system start message.
    with session_maker() as session:
        num_records = session.query(RawMessage).count()
        print(num_records)
        message = Message(device_id="database", content="initial message")
        if num_records == 0:
            session.add(
                RawMessage(
                    id=hash(message),
                    message=json.dumps(message._asdict()),
                    timestamp=datetime.now()
                )
            )
        session.commit()
    
    return session_maker