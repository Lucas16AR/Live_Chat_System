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
        self.rooms = {}  
        
    async def start(self):
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port)

        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader, writer):
        self.clients.append(writer)
        room_name = None

        while True:
            data = await reader.read(100)
            message = data.decode().strip()

            if message.startswith("CREATE "):
                room_name = message.split(" ", 1)[1]
                if room_name not in self.rooms:
                    self.rooms[room_name] = []
                self.rooms[room_name].append(writer)
                continue
            elif message.startswith("JOIN "):
                room_name = message.split(" ", 1)[1]
                if room_name in self.rooms:
                    self.rooms[room_name].append(writer)
                continue

            if message == "QUIT":
                break

            # Supongamos que el mensaje y el alias están separados por '|'
            username, message = message.split('|', 1)

            # Publicar el mensaje en la cola de RabbitMQ
            channel.basic_publish(exchange='',
                                   routing_key='chat_messages',
                                   body=message)

            # Guardar el mensaje en la base de datos
            new_message = Message(username=username, message=message, room_name=room_name)
            session.add(new_message)
            session.commit()

            # Enviar el mensaje a todos los clientes en la sala de este cliente
            if room_name is not None:
                for client in self.rooms[room_name]:
                    client.write(f'({room_name}) {message}'.encode())  # Agregar el nombre de la sala al mensaje

            # Enviar el mensaje a todos los clientes conectados
            for client in self.clients:
                client.write(message.encode())

        writer.close()
        self.clients.remove(writer)
        if room_name is not None:
            self.rooms[room_name].remove(writer)

if __name__ == "__main__":
    chat_server = ChatServer()
    asyncio.run(chat_server.start())