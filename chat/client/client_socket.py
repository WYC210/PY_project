from tkinter.messagebox import showinfo
from config import *
import socket

class ClientSocket(socket.socket):
    # 客户端处理套接字
    def __init__(self):
        # 设置tcp ivp4
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        # 连接服务器
        try:
            super(ClientSocket, self).connect((SEVER_IP,SEVER_PORT))
        except socket.error:
            showinfo('警告',"服务器未响应,程序终止!")
            exit(1)
    def recv_data(self):
        # 接收数据,转换为字符串
        return self.recv(1024).decode('utf-8')
    def send_data(self, message):
        return self.send(message.encode('utf-8'))

