import socket
import threading
import json
import pymongo

#client = pymongo.MongoClient("mongodb://localhost:27017")
client = pymongo.MongoClient("mongodb://mongodb:27017")
db = client["pubsub"]

PORT = 6010
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = socket.gethostbyname('sub1')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 200
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

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
            #msg = json.loads(msg)
            #sender = msg.get("Sender")
            conn.send("Msg received by Subscriber1".encode(FORMAT))

    conn.close()

"""Table with IP details"""
def addtotable():
    ip = db["subscribers"]
    if(not(ip.find_one({"subscriber": "Subscriber1"}))):
        iprecord = {"subscriber":"Subscriber1", "SERVER":SERVER,"PORT":PORT}
        ip.insert_one(iprecord)
    return

def start():
    server.listen()
    addtotable()
    print(f"[LISTENING] Client1 is listening on {SERVER}:{PORT}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING] Client1 is starting...")
start()