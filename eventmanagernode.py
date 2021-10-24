import zmq
import json
from pymongo import MongoClient

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

# Making Connection
myclient = MongoClient("mongodb://localhost:27017/")

# database
db = myclient["GFG"]

# Created or Switched to collection
# names: GeeksForGeeks
Collection = db["data"]

def publish(message):
    socket1 = context.socket(zmq.PUSH)
    socket1.connect("tcp://localhost:6000")
    socket1.send_json(json.dumps(message))
    socket1.close()    
    return 

# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else inser_one is used
if isinstance(message, list):
	Collection.insert_many(message)
else:
	Collection.insert_one(message)


print('Looking out for messages!')
while True:
    socks = dict(poller.poll())
    if socket in socks:
         message = socket.recv_json()
         print(message)
         print("Received below payload from "+ message.get('Sender') +"!!!!")
         publish(message)
         

