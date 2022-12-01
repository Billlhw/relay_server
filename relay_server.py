from aiohttp import web
import socketio
from urllib import parse

clientSessions = dict()

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print("connect ", sid)
    query_params = environ['QUERY_STRING'].split('&')
    params = dict()
    for query_param in query_params:
        k, v = query_param.split('=')
        params[k] = parse.unquote(v)
    client_id = params['client_id']
    print("received client id:", client_id)
    clientSessions[client_id] = sid
    await sio.save_session(sid, {'client_id': client_id})

@sio.event
async def send_message(sid, data):
    print(f"received send message request from client {data['from_client_id']} to client {data['to_client_id']}")
    to_sid = clientSessions[data['to_client_id']]
    if to_sid == None:
        print("target client does not exist") #write into log
        return
    await sio.emit('receive_message', {'message': data['message'], 'from_client_id': 
        data['from_client_id']}, room=to_sid)

@sio.event
def disconnect(sid):
    print('disconnect', sid)

if __name__ == '__main__':
    web.run_app(app, host="127.0.0.1", port="5000")
    