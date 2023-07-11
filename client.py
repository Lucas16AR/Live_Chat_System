import asyncio

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

        alias = input("Enter your alias: ")

        while True:
            try:
                message = input("Enter message: ")
                print(f'Sending: {message!r}')
                writer.write(f'{alias}|{message}'.encode())

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