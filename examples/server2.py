import asyncio
import socket
from collections import deque

# Cola de tareas distribuidas para gestionar los mensajes entrantes
message_queue = deque()


async def handle_client(reader, writer):
    # Función asincrónica para manejar la comunicación con un cliente

    # Se recibe el nombre de usuario del cliente
    username = await reader.readline()
    username = username.decode().strip()

    # Se notifica a todos los clientes conectados que un nuevo usuario se ha unido
    message = f"{username} se ha unido al chat\n".encode()
    broadcast(message, writer)

    try:
        while True:
            # Se espera a recibir un mensaje del cliente
            message = await reader.readline()
            if not message:
                break

            # Se notifica a todos los clientes conectados el mensaje recibido
            broadcast(message, writer)

    except asyncio.CancelledError:
        pass
    finally:
        # Se notifica a todos los clientes que el usuario ha abandonado el chat
        message = f"{username} ha abandonado el chat\n".encode()
        broadcast(message, writer)

        # Se cierra la conexión con el cliente
        writer.close()
        await writer.wait_closed()


def broadcast(message, sender):
    # Función para enviar un mensaje a todos los clientes conectados

    for writer in active_clients:
        if writer != sender:
            writer.write(message)


async def message_dispatcher():
    # Función asincrónica para distribuir los mensajes de la cola a los clientes

    while True:
        if message_queue:
            message = message_queue.popleft()
            await broadcast(message, None)
        await asyncio.sleep(0.1)


async def main():
    # Función principal del servidor

    # Configuración del servidor
    host = 'localhost'
    port = 8888

    server = await asyncio.start_server(
        handle_client, host, port)

    print(f'Servidor de chat en tiempo real iniciado en {host}:{port}')

    async with server:
        await asyncio.gather(server.serve_forever(), message_dispatcher())


# Lista para almacenar los clientes conectados
active_clients = set()

if __name__ == '__main__':
    asyncio.run(main())
