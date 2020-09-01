#!/bin/python

import cv2
import socket
import numpy as np
import hashlib

DURATION = 1000 # Unit: ms
DEVICE_NUM = 0
SERVER = {
    'HOST': '127.0.0.1',
    'PORT': 3000
}

cap = cv2.VideoCapture(DEVICE_NUM)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

while(True):
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    _, frame = cap.read()
    cv2.imshow('Capture', frame)

    # Upload image to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER['HOST'], SERVER['PORT']))
    _, encoded_img = cv2.imencode('.jpeg', frame)
    encoded_img = bytes(encoded_img)
    
    # Calculate the length of data
    data_len = len(encoded_img)
    print('Length:', len(encoded_img), 'bytes')
    data_len = data_len.to_bytes(4, byteorder="little")
    print(data_len)
    
    # Send data length & data
    client.sendall(data_len+encoded_img) 
    
    hash_gen = hashlib.md5()
    hash_gen.update(encoded_img)
    hash_val = hash_gen.hexdigest()
    print('MD5:', hash_val)
    
    #img_bytes = np.frombuffer(encoded_img, dtype=np.uint8)
    #img_bytes = img_bytes.reshape(-1,1)
    
    #img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
    #cv2.imshow('Server', img)

    serverMessage = str(client.recv(1024), encoding='utf-8')
    print('Server:', serverMessage)

    client.close()
    if cv2.waitKey(DURATION) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()