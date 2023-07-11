from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine('sqlite:///chat.db', echo=True)
Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def save_message(username, message):
    new_message = Message(username=username, message=message)
    session.add(new_message)
    session.commit()

def get_all_messages():
    messages = session.query(Message).all()
    return messages
