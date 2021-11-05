import socket
import threading
import json

PORT = 6020
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = socket.gethostbyname('client')
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
            conn.send("Msg received by Subscriber3".encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Client3 is listening on {SERVER}:{PORT}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING] Client3 is starting...")
start()