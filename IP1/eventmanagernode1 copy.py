import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '0.0.0.0'
port = 4500
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    print('Received:'+ str(Client.recv(1024)))
    start_new_thread(threaded_client, (Client, ))
ServerSocket.close()