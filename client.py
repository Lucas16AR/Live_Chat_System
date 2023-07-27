import socketio
import threading
import clear

sio = socketio.Client()

username = None
room = None
clear.clear()

@sio.event
def connect():
    global username, room
    print('Conexión establecida')
    username = input('Escriba su nombre de usuario: ')
    room = input('Escribe el nombre de la sala a la cual quieres ingresar o crear: ')
    print(f'Se ha unido a la sala: {room}')
    sio.emit('join', {'username': username, 'room': room})

@sio.event
def message(data):
    print('Mensaje recibido: ', data)

@sio.event
def disconnect():
    print('Desconectado del servidor')

def send_message():
    global username, room
    while True:
        message = input('Escribe tu mensaje: ')
        if message == 'QUIT':
            sio.emit('leave', {'username': username, 'room': room})
            print('Has dejado la sala.')
            break
        elif message == 'EXIT':
            sio.disconnect()
            print('Te has desconectado del servidor.')
            break
        else:
            sio.emit('message', {'username': username, 'message': message, 'room': room})

if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    threading.Thread(target=send_message).start()
    sio.wait()