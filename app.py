#!/usr/bin/env python

from flask import Flask, render_template, Response
from imutils.video import VideoStream
import imutils
import cv2
import datetime
import socket
import numpy as np

app = Flask(__name__)
# vs = VideoStream('http://camera.butovo.com/mjpg/video.mjpg').start()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 9094))
sock.listen(1)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    conn, addr = sock.accept()
    many_bytes = 1024
    while True:
        data = b''
        size = conn.recv(1024)
        strings = size.decode('utf8')
        int_size = int(strings)
        conn.send('recieved'.encode('utf8'))
        while True:
            part = conn.recv(many_bytes)
            data += part
            if len(data) == int_size:
                break
        print('received')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
