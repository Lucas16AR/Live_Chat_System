import asyncio
import sys


async def send_message(reader, writer):
    # Función asincrónica para enviar mensajes al servidor

    while True:
        message = input("> ")
        writer.write(message.encode())
        await writer.drain()


async def receive_messages(reader, writer):
    # Función asincrónica para recibir mensajes del servidor

    try:
        while True:
            message = await reader.readline()
            if not message:
                break
            print(message.decode(), end='')
    except asyncio.CancelledError:
        pass


async def main():
    # Función principal del cliente

    # Configuración del servidor
    host = 'localhost'
    port = 8888

    try:
        reader, writer = await asyncio.open_connection(host, port)

        # Se solicita al cliente que ingrese su nombre de usuario
        username = input("Ingrese su nombre de usuario: ")
        writer.write(username.encode())
        await writer.drain()

        tasks = [
            asyncio.create_task(send_message(reader, writer)),
            asyncio.create_task(receive_messages(reader, writer))
        ]

        await asyncio.gather(*tasks)
    except (ConnectionRefusedError, ConnectionResetError):
        print("No se pudo establecer una conexión con el servidor")
    finally:
        writer.close()
        await writer.wait_closed()
        sys.exit()


if __name__ == '__main__':
    asyncio.run(main())
