#!/bin/python
import cv2
import socket
import numpy as np
import hashlib
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

    print('Received new capture')
    img_bytes = recvall(conn)

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