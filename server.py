import asyncio
import socket
from requests import session
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
import pika

# Definir el modelo de la base de datos
Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    username = Column(String (100))
    message = Column(String (100))
    timestamp = Column(DateTime, default=func.now())

# Conectar a la base de datos
engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(bind=engine)

# Crear una sesión de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

#def save_message(username, message, timestamp):
#    try:
#        new_message = Message(username=username, message=message, timestamp=timestamp)
#        session.add(new_message)
#        session.commit()
#    except Exception as e:
#        print(f"Error saving message: {e}")
#
#def get_all_messages():
#    message = session.query(Message).all()
#    return message

# Conectar a RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='chat_messages')

class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.bind((self.host, self.port))
        self.server.listen()
        self.server = None
        self.clients = []

    async def start(self):
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port)

        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader, writer):
        self.clients.append(writer)

        while True:
            data = await reader.read(100)
            message = data.decode().strip()

            if message == "QUIT":
                break

            # Supongamos que el mensaje y el alias están separados por '|'
            username, message = message.split('|', 1)

            # Publicar el mensaje en la cola de RabbitMQ
            channel.basic_publish(exchange='',
                                   routing_key='chat_messages',
                                   body=message)

            # Guardar el mensaje en la base de datos
            new_message = Message(username=username, message=message)
            session.add(new_message)
            session.commit()
            
            # Enviar el mensaje a todos los clientes conectados
            for client in self.clients:
                client.write(message.encode())

        writer.close()
        self.clients.remove(writer)

if __name__ == "__main__":
    chat_server = ChatServer()
    asyncio.run(chat_server.start())