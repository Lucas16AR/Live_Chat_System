import clear
import socketio
import threading

sio = socketio.Client()

username = None
room = 'common_room'

@sio.event
def connect():
    clear.clear()
    global username
    print('Conexión establecida')
    username = input('Escriba su nombre de usuario: ')
    print(f'Se ha unido a la sala: {room}')
    sio.emit('join', {'username': username})

@sio.event
def messages(data):
    print(f'{data["username"]}: {data["message"]}')
    print('Se activó el evento \'message\' en el cliente.')

@sio.event
def disconnect():
    print('Desconectado del servidor')

def send_message():
    global username
    while True:
        message = input('Escribe tu mensaje: ')
        if message == 'QUIT':
            sio.emit('leave', {'username': username, 'room': room})
            print('Has dejado la sala.')
            break
        elif message == 'EXIT':
            sio.disconnect()
            print('Te has desconectado del servidor.')
            exit()
        else:
            sio.emit('message', {'username': username, 'message': message, 'room': room})

if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    threading.Thread(target=send_message).start()
    sio.wait()