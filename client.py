import socketio
import sys

sio = socketio.Client()
client_id = 0

@sio.event
def connect():
    print('connection established')

@sio.on('receive_message')
def receive_message(data):
    print(f"received message \"{data['message']}\" from client {data['from_client_id']}")

@sio.event
def disconnect():
    print('disconnected from server')

#./client.py from_client_id -s to_client_id
if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print("Please enter client id")
        exit()

    client_id = argv[1]
    sio.connect(f"http://localhost:5000/join?client_id={client_id}")
    if len(argv) == 4:
        sio.emit('send_message', {'message': f"client {client_id} message", 
            'from_client_id': client_id, 'to_client_id': argv[3]})
    sio.wait()
