import socket
import threading

class Client:
    def __init__(self, host = '127.0.0.1', port = 55555):
        self.nickname = input('Enter your nickname: ')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    print(message)
            except:
                print('Error!')
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.nickname}: {input("> ")}'
            self.client.send(message.encode('ascii'))

    def startChat(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()


if __name__ == "__main__":
    client = Client()
    client.startChat()