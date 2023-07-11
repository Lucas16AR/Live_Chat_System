import socket
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    alias = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('sqlite:///chat.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def handle_client(conn, addr):
    print(f"Connection from {addr} has been established.")
    while True:
        msg = conn.recv(1024).decode("utf8")
        if msg != "":
            alias, message = msg.split(": ")
            try:
                new_message = Message(alias=alias, message=message)
                session.add(new_message)
                session.commit()
            except Exception as e:
                print(f"Error saving message: {e}")

    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 55555))
    server.listen()
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)

if __name__ == "__main__":
    start_server()
