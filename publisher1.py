import time
import requests
import json
import zmq
import socket 

"""Publisher for TESLA's Stock Price"""
url = "https://realstonks.p.rapidapi.com/TSLA"
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://127.0.0.1:5555")

headers = {
    'x-rapidapi-host': "realstonks.p.rapidapi.com",
    'x-rapidapi-key': "6c88faa169mshf884cd03d448ab2p151f28jsne5865b21021b"
    }
def Publish():
    response = requests.request("GET", url, headers=headers)
    message = json.loads(response.text)
    #print(message)
    message = json.loads(message)
    #print(type(message))
    message["Topic"] = "Tesla stock price"
    message["Sender"] = "Publisher1"
    print('Publisher1 sending Payload:' + json.dumps(message))
    socket.send_json(message)
    #db = client.get_database('total_records')
    #records = db.register
    return
    
if __name__ == "__main__":
    time.sleep(3)
    while(1):
        Publish()
        time.sleep(15)
