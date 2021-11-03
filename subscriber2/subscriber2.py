import zmq
import socket
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:6010")          
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
print('Looking out for messages!')
while True:
    socks = dict(poller.poll())
    if socket in socks:
         message = socket.recv_json()
         print(message)
         print("Received message on topic "+ message.get('Topic'))
