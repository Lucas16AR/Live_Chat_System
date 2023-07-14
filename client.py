import asyncio
from aioconsole import ainput
import threading
import logging
import clear

# Crear un bloqueo
console_lock = threading.Lock()

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.console_lock = asyncio.Lock()
        self.username = None  # Agrega esto

    async def start(self):
        clear.clear()
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(self.host, self.port), timeout=10)
        except (ConnectionRefusedError, TimeoutError, OSError):
            print("Error: Unable to connect to the server")
            return

        self.username = await ainput("Enter your alias: ")  # Modifica esta línea  
        
        while True:
            command = await ainput("Enter a command (CREATE ~room_name~ or JOIN ~room_name~): ")
            if command.startswith("CREATE ") or command.startswith("JOIN "):
                writer.write(command.encode())
                print(f"Success ({command})")
                break
            else:
                print("Invalid command")
        
        handled = False
        while not handled:
            # Manejar el mensaje de unirse a la sala
            if command.startswith("CREATE") or command.startswith("JOIN"):
                room_name = command.split(" ", 1)[1]
                print(f"Room {room_name}")
                handled = True
            else:
                print("Invalid command")
                command = await ainput("Enter a command (CREATE room_name or JOIN room_name): ")

        listen_task = asyncio.create_task(self.listen(reader))  # Crear tarea para escuchar mensajes
        send_task = asyncio.create_task(self.send(writer))  # Crear tarea para enviar mensajes

        await asyncio.gather(listen_task, send_task)  # Ejecutar ambas tareas en paralelo
    
    async def listen(self, reader):
        while True:
            try:
                data = await reader.read(100)
                if data:
                    message = data.decode().strip()
                    print(f'Received message: {message}', flush=True)  # Asegúrate de que los mensajes se impriman inmediatamente
                else:
                    break
            except Exception as e:
                print(f'Error: {e}')
                break
    
    async def send(self, writer):
        while True:
            try:
                message = await ainput("Enter message: ")
                print(f'Sending: {message!r}')
                writer.write(f'{self.username}|{message}'.encode())
                if message == 'QUIT':
                    print('Closing the connection')
                    writer.close()
                    break
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                print("Error: Connection lost")
                break
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    chat_client = ChatClient()
    asyncio.run(chat_client.start())