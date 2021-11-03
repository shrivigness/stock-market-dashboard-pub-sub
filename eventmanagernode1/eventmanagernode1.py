import zmq
import json
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017")
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://0.0.0.0:5555")
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

def publish(message):
    socket1 = context.socket(zmq.PUSH)
    socket1.connect("tcp://0.0.0.0:6010")
    print(message)
    del message["_id"]
    print(message)
    socket1.send_json(json.dumps(message))
    socket1.close()    
    return 

def storerawdata(payload):
    db = client.get_database('pubsub')
    rawdata = db.get_collection('rawdata')
    rawdata.insert_one(payload)
    return 

print('Looking out for messages!')
while True:
    socks = dict(poller.poll())
    if socket in socks:
         message = socket.recv_json()
         print(message)
         print("Received below payload from "+ message.get('Sender') +"!!!!")
         storerawdata(message)
         print("Stored Data in DB")
         publish(message)