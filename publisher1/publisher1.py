import time
import requests
import json
import zmq
import socket 

"""Publisher for Amazon's stock summary"""

url = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary"
querystring = {"symbol":"AMZN","region":"US"}

headers = {
    'x-rapidapi-host': "yh-finance.p.rapidapi.com",
    'x-rapidapi-key': "6c88faa169mshf884cd03d448ab2p151f28jsne5865b21021b"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
#def Advertise():
#    return
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://localhost:5555")

def Publish():
    response = requests.request("GET", url, headers=headers, params=querystring)
    message = response.json()
    message["Topic"] = 'Amazon stock summary'
    message["Sender"] = 'Publisher1'
    print('Publisher1 sending Payload:' + json.dumps(message))
    socket.send_json(message)
    return


if __name__ == "__main__":
    time.sleep(3)
    while(1):
        Publish()
        time.sleep(15)
    socket.close()
