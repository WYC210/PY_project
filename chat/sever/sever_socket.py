import socket
from config import *


class ServerSocket(socket.socket):
    def __init__(self):
        # 设置为TCP
        super(ServerSocket,self).__init__(socket.AF_INET,socket.SOCK_STREAM)
        # 绑定地址 和端口号
        self.bind((SEVER_IP,SEVER_PORT))
        self.listen(128)