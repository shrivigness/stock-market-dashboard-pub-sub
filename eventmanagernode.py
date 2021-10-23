import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

def publish(message):
    socket1 = context.socket(zmq.PUSH)
    socket1.connect("tcp://localhost:6000")
    socket1.send_json(json.dumps(message))
    socket1.close()    
    return 

print('Looking out for messages!')
while True:
    socks = dict(poller.poll())
    if socket in socks:
         message = socket.recv_json()
         print(message)
         print("Received below payload from "+ message.get('Sender') +"!!!!")
         publish(message)
         

