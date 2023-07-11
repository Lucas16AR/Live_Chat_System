from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    username = Column(String (100))
    message = Column(String (100))
    room_name = Column(String (100))
    timestamp = Column(DateTime, default=func.now())

engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def save_message(username, message, room_name):
    new_message = Message(username=username, message=message, room_name=room_name)
    session.add(new_message)
    session.commit()

def get_all_messages():
    messages = session.query(Message).all()
    return messages