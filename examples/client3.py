import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 55555))
    while True:
        alias = input("Enter your alias: ")
        message = input("Enter your message: ")
        client.send(f"{alias}: {message}".encode("utf8"))

if __name__ == "__main__":
    start_client()
