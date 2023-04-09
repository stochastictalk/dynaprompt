from sqlalchemy import Column, Integer, String, DateTime

from dynaprompt._Base import Base

# Define the model for the table
class RawMessage(Base):
    __tablename__ = "raw_messages"

    id = Column(Integer, primary_key=True)
    message = Column(String)
    timestamp = Column(DateTime)