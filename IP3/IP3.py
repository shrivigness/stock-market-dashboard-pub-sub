import socket
import threading
import json
import pymongo

#client = pymongo.MongoClient("mongodb://localhost:27017")
client = pymongo.MongoClient("mongodb://mongodb:27017")
db = client["pubsub"]

"""Network Details of IP3"""
PORT = 5060
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = socket.gethostbyname('IP3')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 200

"""Network Details of Client3"""
CPORT = 6020
#CSERVER = "192.168.56.1"
CSERVER = socket.gethostbyname('sub3')
CADDR = (CSERVER, CPORT)
FORMAT = 'utf-8'
HEADER = 200
#DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

"""Publishers Publishing to IP3"""
publishers = ["Publisher7","Publisher8","Publisher9"]

def senddata(msg,server,port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (server, port)
    client.connect(address)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    pass

"""
def storerawdata(payload):
    db = client.get_database('pubsub')
    rawdata = db.get_collection('rawdata')
    rawdata.insert_one(payload)
"""

"""Notify newly published Data"""

def notify(msg):
    topiclist = db["topics"]
    sublist = db["subscribers"]
    for subs in topiclist.find({"topic":msg["Topic"]}):
        if(subs["subscriber"]=="Subscriber3"):
            senddata(json.dumps(msg),CSERVER,CPORT)
        else:
            subrecord = sublist.find_one({"subscriber":subs["subscriber"]})
            senddata(json.dumps(msg),subrecord["SERVER"],subrecord["PORT"])
    return

"""Subscriber-3 Subscribes to a Topic"""

def subscribe(msg):
    topiclist = db["topics"]
    if(not(topiclist.find_one({"topic":msg["Topic"],"IP":"IP3", "subscriber":"Subscriber3"}))):
        iprecord = {"topic":msg["Topic"],"IP":"IP3", "subscriber":"Subscriber3"}
        topiclist.insert_one(iprecord)
    return

"""Subscriber-3 Unsubscribes to a Topic"""

def unsubscribe(msg):
    topiclist = db["topics"]
    if(topiclist.find_one({"topic":msg["Topic"],"IP":"IP3", "subscriber":"Subscriber3"})):
        topiclist.delete_one({"topic":msg["Topic"],"IP":"IP3", "subscriber":"Subscriber3"})
    return

"""Advertise a new Topic"""

def advertise(msg):
    publisher = msg["Sender"]
    if(publisher in publishers):
        advertisemsg = msg["Topic"]+" is available for Subscription"
        msg["Adverstisemsg"] = advertisemsg
        msg["IP"] = "IP3"
        senddata(json.dumps(msg),CSERVER,CPORT)
        ip = db["IPs"]
        for iprecord in ip.find():
            if(iprecord["IP"]!="IP3"):
                senddata(json.dumps(msg),iprecord["SERVER"],iprecord["PORT"])
    else:
        senddata(json.dumps(msg),CSERVER,CPORT)
    return

"""Handle incoming messages"""

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
            if("Advertise" in msg):
                advertise(msg)
            elif("Subscribe" in msg):
                subscribe(msg)
            elif("Unsubscribe" in msg):
                unsubscribe(msg)
            else:
                notify(msg)
            sender = msg.get("Sender")
            conn.send("Msg received by IP3".encode(FORMAT))
    conn.close()

"""Table with IP details"""
def addtotable():
    db = client.get_database('pubsub')
    ip = db["IPs"]
    if(not(ip.find_one({"IP": "IP3"}))):
        iprecord = {"IP":"IP3", "SERVER":SERVER,"PORT":PORT}
        ip.insert_one(iprecord)
    return

"""Handle incoming messages"""

def start():
    server.listen()
    addtotable()
    print(f"[LISTENING] IP3 is listening on {SERVER}:{PORT}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING] IP3 is starting...")
start()