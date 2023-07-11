import asyncio
from aioconsole import ainput

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port

    async def start(self):
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(self.host, self.port), timeout=10)
        except (ConnectionRefusedError, TimeoutError, OSError):
            print("Error: Unable to connect to the server")
            return

        username = await ainput("Enter your alias: ")  
        
        while True:
            command = await ainput("Enter a command (CREATE room_name or JOIN room_name, or SEND message): ")
            if command.startswith("CREATE ") or command.startswith("JOIN "):
                writer.write(command.encode())
                print(f"Success ({command})")
            elif command == "SEND":
                break
            else:
                print("Invalid command")

        while True:
            try:
                message = await ainput(f"({room_name}) Enter message: ")
                print(f'Sending: {message!r}')
                writer.write(f'{username}|{message}'.encode())

                if message == 'QUIT':
                    print('Closing the connection')
                    writer.close()
                    break
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                print("Error: Connection lost")
                break

if __name__ == "__main__":
    chat_client = ChatClient()
    asyncio.run(chat_client.start())