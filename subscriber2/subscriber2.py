import socket
import threading
import json
import pymongo

#client = pymongo.MongoClient("mongodb://localhost:27017")
client = pymongo.MongoClient("mongodb://mongodb:27017")
db = client["pubsub"]

PORT = 6015
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = socket.gethostbyname('sub2')
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
            conn.send("Msg received by Subscriber2".encode(FORMAT))
            msg = json.loads(msg)
            if("Advertise" in msg):
                coll = db["topics_list"]
                if(not(coll.find_one({"topic":msg["Topic"]}))):
                    coll.insert_one({"topic":msg["Topic"],"IP":msg["IP"],"sender":msg["Sender"]})
            else:
                coll = db["subscriber2_rawdata"]
                coll.insert_one(msg)
    conn.close()

"""Table with IP details"""
def addtotable():
    ip = db["subscribers"]
    if(not(ip.find_one({"subscriber": "Subscriber2"}))):
        iprecord = {"subscriber":"Subscriber2", "SERVER":SERVER,"PORT":PORT}
        ip.insert_one(iprecord)
    return


def start():
    server.listen()
    addtotable()
    print(f"[LISTENING] Client2 is listening on {SERVER}:{PORT}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print(f"[STARTING] Client2 is starting...")
start()