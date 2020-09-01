#!/bin/python
import cv2
import socket
import numpy as np
SERVER = {
    'HOST': '0.0.0.0',
    'PORT': 3000
}

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER['HOST'], SERVER['PORT']))
server.listen(10)

while True:
    conn, addr = server.accept()
    img_bytes = recvall(conn)

    img_bytes = np.frombuffer(img_bytes, dtype=np.uint8)
    img_bytes = img_bytes.reshape(-1,1)

    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    cv2.imshow('Server', img)

    print('Received new capture')

    serverMessage = 'Capture saved';
    conn.sendall(serverMessage.encode())
    conn.close()