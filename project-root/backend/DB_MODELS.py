from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
import json
from sqlalchemy.types import TypeDecorator, TEXT

Base = declarative_base()

class JSONEncodedList(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return '[]'
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        return json.loads(value)

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    text = Column(Text, nullable=False)
    summary = Column(Text)
    entities = Column(JSONEncodedList)  # Stored as JSON string
    sentiment = Column(String)

    def __repr__(self):
        return f"<Document(filename={self.filename}, sentiment={self.sentiment})>"
