import datetime
import socket

import cv2
import imutils
import numpy as np

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 9093))
sock.listen(1)
many_bytes = 4096
shape_size_bytes = 12
confirm_message_size = len('recieved'.encode('utf8'))

sock_to_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_to_send.connect(('127.0.0.1', 9094))

while 1:
    conn, addr = sock.accept()
    print('Клиент подключен: ', addr[0])
    data = b''
    size = conn.recv(1024)
    strings = size.decode('utf8')
    int_size = int(strings)

    while True:
        while True:
            part = conn.recv(many_bytes)
            data += part
            if len(data) == int_size:
                break
        image = np.frombuffer(data, dtype=np.uint8)
        data = b''
        frame = np.resize(image, (576, 704, 3))
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10, 500)
        fontScale = 1
        fontColor = (255, 255, 255)
        lineType = 2
        now = datetime.datetime.now()
        cv2.putText(frame, now.strftime("%Y-%m-%d %H:%M:%S"),
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)
        frame = imutils.resize(frame, width=800, height=900)
        frame = cv2.bitwise_not(frame)
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        print('recieved')

        sock_to_send.send(str(len(encodedImage)).encode('utf8'))
        ans = sock_to_send.recv(confirm_message_size)
        sock_to_send.send(bytearray(encodedImage))

        conn.send('recieved'.encode('utf8'))
