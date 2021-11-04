import socket
import threading
import json
import pymongo

#client = pymongo.MongoClient("mongodb://localhost:27017")
"""Network Details of IP1"""
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = socket.gethostbyname('IP1')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 200

"""Network Details of Client1"""
CPORT = 6010
#CSERVER = "192.168.56.1"
CSERVER = socket.gethostbyname('client')
CADDR = (CSERVER, CPORT)
FORMAT = 'utf-8'
HEADER = 200
#DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
"""
def storerawdata(payload):
    db = client.get_database('pubsub')
    rawdata = db.get_collection('rawdata')
    rawdata.insert_one(payload)
"""
def publish(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(CADDR)
    #del msg["_id"] 
    msg = json.dumps(msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    return

def subscribe():
    return

def unsubscribe():
    return

def notify(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(CADDR)
    notifymsg = msg["Topic"]+" is avilable for Subscription" 
    message = notifymsg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    return

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(HEADER).decode(FORMAT)
            connected = False
            print(f"[{addr}]{msg}")
            msg = json.loads(msg)
            if("Notify" in msg):
                notify(msg)
            else:
                #storerawdata(msg)
                publish(msg)
            sender = msg.get("Sender")
            conn.send("Msg received by IP1".encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] IP1 is listening on {SERVER}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING] IP1 is starting...")
start()