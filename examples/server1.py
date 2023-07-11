import socket
import threading
from database import save_message, get_all_messages

class Server:
    def __init__(self, host = '127.0.0.1', port = 55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.clients = {}
        self.nicknames = {}

    def broadcast(self, message, source, room):
        for client in self.clients[room]:
            if client != source:
                client.send(message)

    def handle(self, client, room):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message, client, room)
            except:
                index = self.clients[room].index(client)
                self.clients[room].remove(client)
                client.close()
                nickname = self.nicknames[room][index]
                self.nicknames[room].remove(nickname)
                self.broadcast(f'{nickname} left the chat!'.encode('ascii'), None, room)
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')

            client.send('ROOM'.encode('ascii'))
            room = client.recv(1024).decode('ascii')
            if room not in self.clients:
                self.clients[room] = []
                self.nicknames[room] = []

            self.nicknames[room].append(nickname)
            self.clients[room].append(client)

            print(f'Nickname of the client is {nickname}!')
            self.broadcast(f' {nickname} joined the chat!'.encode('ascii'), None, room)
            client.send(' Connected to the server!'.encode('ascii'))

            thread = threading.Thread(target=self.handle, args=(client, room))
            thread.start()

if __name__ == "__main__":
    server = Server()
    server.receive()