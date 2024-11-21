class SocketWrapper(object):
    def __init__(self,sock):
        self.sock=sock
    def recv_data(self):
        #接受发送数据
        try:
            return self.sock.recv(1024).decode('UTF-8')
        except:
            return ''
    def send_data(self, data):
        #发送数据
        return self.sock.send(data.encode('UTF-8'))

    def close(self):
        #关闭套接字
        self.sock.close()