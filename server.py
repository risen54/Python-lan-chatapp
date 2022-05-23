import socket
import threading
import json
from ByteArray import ByteArray

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def xor(key: int, data: bytearray):
    '''Something you should not try to play around with, ignore it'''
    key &= 0xFFFF
    key <<= key & 5
    return bytearray([(byte ^ key) & 0xFF for byte in data])


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    msgs = []

    connected = True
    while connected:
        msg = conn.recv(1024)
        msg = xor(123456, msg)
        msg = msg.decode()
        msgs.append(msg)

        if len(msg) == 0:
            connected = False
        else:
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            msgs = bytearray(str(msgs).encode())
            msgs = xor(123456, msgs)
            conn.send(msgs)

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
