import socket
import json
from ByteArray import ByteArray

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client.setblocking(False)

def xor(key: int, data: bytearray):
    '''Something you should not try to play around with, ignore it'''
    key &= 0xFFFF
    key <<= key & 5
    return bytearray([(byte ^ key) & 0xFF for byte in data])

def send(msg, name):
    data = {"sender": name, "msg": msg}
    data = bytearray(str(data).encode())
    msg = xor(123456, data)
    client.send(msg)

name = "Satvik"

def start():
    while True:
        msg = input("> ")

        if msg:
            send(msg, name)
            if msg == DISCONNECT_MESSAGE:
                exit()

        msgs = client.recv(1024)
        msgs = xor(123456, msgs)
        msgs = msgs.decode()
        for msg in msgs:
            print(msg)
start()
