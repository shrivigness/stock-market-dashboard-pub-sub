import time
import requests
import json
import socket 

HEADER = 200
PORT = 5060
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
#SERVER = "192.168.56.1"
SERVER = socket.gethostbyname('IP3')
ADDR = (SERVER, PORT)


"""Publisher for Netflix Inc's Stock Price"""
url = "https://realstonks.p.rapidapi.com/NFLX"

headers = {
    'x-rapidapi-host': "realstonks.p.rapidapi.com",
    'x-rapidapi-key': "6c88faa169mshf884cd03d448ab2p151f28jsne5865b21021b"
    }

def advertise():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    msg = '{"Sender":"Publisher9", "Topic":"Netflix Inc stock price", "Advertise":true}'
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    return
def send(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    return

def Publish():
    response = requests.request("GET", url, headers=headers)
    message = json.loads(response.text)
    #print(message)
    message = json.loads(message)
    #print(type(message))
    message["Topic"] = "Netflix Inc stock price"
    message["Sender"] = "Publisher9"
    print('Publisher9 sending Payload:' + json.dumps(message))
    send(json.dumps(message))
    #db = client.get_database('total_records')
    #records = db.register
    return
    
if __name__ == "__main__":
    time.sleep(3)
    advertise()
    while(1):
        Publish()
        time.sleep(15)
