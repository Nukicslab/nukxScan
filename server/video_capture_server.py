#!/bin/python
import cv2
import socket
import numpy as np
import hashlib
import binascii

SERVER = {
    'HOST': '0.0.0.0',
    'PORT': 3000
}

def recvFrame(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    data_len = -1
    while True:
        part = sock.recv(BUFF_SIZE)
        if data_len == -1:
            data_len = int.from_bytes(part[0:4], byteorder='little')
            data += part[4:]
        else:
            data += part
        if len(data) == data_len:
            # Received whole frame
            break
    return data

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER['HOST'], SERVER['PORT']))
server.listen(10)

while True:
    conn, addr = server.accept()

    print('Received new capture')
    img_bytes = recvFrame(conn)

    print('Length:', len(img_bytes), 'bytes')
    hash_gen = hashlib.md5()
    hash_gen.update(img_bytes)
    hash_val = hash_gen.hexdigest()
    print('MD5:', hash_val)

    img_bytes = np.frombuffer(img_bytes, dtype=np.uint8)
    img_bytes = img_bytes.reshape(-1,1)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    cv2.imshow('Server', img)
    cv2.waitKey(1) # Must write this after imopen

    serverMessage = 'Capture received MD5: '+hash_val
    conn.sendall(serverMessage.encode())
    conn.close()

cv2.destroyAllWindows()