from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///chat.db')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    message = Column(String(500))
    room = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __init__(self, username, message, room):
        self.username = username
        self.message = message
        self.room = room