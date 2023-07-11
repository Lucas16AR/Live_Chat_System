import asyncio
import socket
from requests import session
from database import session, Message
import pika


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