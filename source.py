import socket
from imutils.video import VideoStream

vs = VideoStream('http://camera.butovo.com/mjpg/video.mjpg').start()

confirm_message_size = len('recieved'.encode('utf8'))

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 9093))
    print('Подключен')
    image = vs.read()
    image_bytes = image.tobytes()
    sock.send(str(len(image_bytes)).encode('utf8'))
    while True:
        image = vs.read()
        image_bytes = image.tobytes()
        sock.send(image_bytes)
        ans = sock.recv(confirm_message_size)


except ConnectionRefusedError:
    print('Подключение не установлено')


