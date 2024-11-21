import socket
from datetime import datetime



def text():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 9494))
    while True:
        msg = input("输入内容")
        # 获取当前时间戳（秒级）
        timestamp = int(datetime.now().timestamp())
        # formatted_timestamp = format(timestamp, '016x')
        # message = msg + '|' + formatted_timestamp
        s.send(msg.encode('utf-8'))
        recv_data = s.recv(1024)
        print(recv_data.decode('utf-8'))

text()
