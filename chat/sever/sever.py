
from sever_socket import  ServerSocket
from Socket_Wrapper import SocketWrapper
from threading import Thread
from response_protocol import *
from config import *
from db import DB
class Server(object):
    def __init__(self):
        #初始化
        self.sever_socket = ServerSocket()
        # 根据传过来的ID进行不同操作
        # 根据不同类型执行不同操作
        self.requests_handle_function = {}
        self.register(REQUEST_LOGIN,self.request_login)
        self.register(REQUEST_CHAT,self.request_chat)
        self.register(REQUEST_REGISTER,self.request_register)
        self.register(REQUEST_CHANGE,self.request_change)
        # 登录的用户
        self.clients={}
        # 初始化数据库类
        self.db = DB()
        # 存储离线玩家名称
        self.out_name = ''
    def register(self,request_id,fun):
        self.requests_handle_function[request_id] = fun
    def startup(self):
        while True:
            print("正在等待连接")
            soc,add = self.sever_socket.accept()
            print("链接成功")
            # 接收套接字
            client_soc = SocketWrapper(soc)
            Thread(target=lambda: self.request_header(client_soc)).start()


    def request_header(self,client_soc):
        # 处理客户端请求

        while True:
            msg = client_soc.recv_data()
            if not msg:
                self.remove_user(client_soc)
                # 没有接收到消息
                client_soc.close()
                break
            # 处理发送过来的信息
            pars = self.parse_request_text(msg)
            handle_function = self.requests_handle_function.get(pars['request_id'])


            if handle_function:
                handle_function(client_soc,pars)

    def remove_user(self, client_soc):
        print("离线")
        print(client_soc)
        print(self.clients)

        # 初始化nickname为默认值
        nickname = None

        # 有账号离线就删除对应的套接字
        for username, info in self.clients.items():
            print(info['sock'])
            print(client_soc)
            if info['sock'] == client_soc:
                self.out_name = username
                nickname = info['nickname']  # 获取离线用户的昵称
                del self.clients[username]
                break

        # 如果未找到用户，打印警告并返回
        if nickname is None:
            print(f"警告: 未找到匹配的客户端套接字 {client_soc}")
            return

        print("离线")
        print(client_soc)
        print(self.clients)

        # 拼接发送的字符串
        msg = ResponseProtocol.response_chat('系统消息', '系统消息', f'{nickname}离开了QAQ', 'ALL')

        # 把字符串发送给所有人
        for u_name, info in self.clients.items():
            info['sock'].send_data(msg)

    def parse_request_text(self, msg):
        request_list = msg.split(DELIMITER)
        request_dict = {}
        print(request_list)
        request_dict['request_id'] = request_list[0]
        if request_dict['request_id'] == REQUEST_LOGIN:
            # 登录请求
            request_dict['username'] = request_list[1]
            request_dict['password'] = request_list[2]

        elif request_dict['request_id'] == REQUEST_CHAT:
            # 聊天请求
            request_dict['nickname'] = request_list[1]
            request_dict['username'] = request_list[2]
            request_dict['messages'] = request_list[3]
            request_dict['to_user'] = request_list[4]
        elif request_dict['request_id'] == REQUEST_REGISTER:
            # 注册请求
            request_dict['username'] = request_list[1]
            request_dict['password'] = request_list[2]
            request_dict['nickname'] = request_list[3]
        elif request_dict['request_id'] == REQUEST_CHANGE:
            # 更换聊天人请求
            request_dict['username'] = request_list[1]
            request_dict['other'] = request_list[2]
        print('解析完的数据')
        print(request_dict)
        return request_dict

    def request_login(self,client_soc,request_data):

        # 处理登录请求
        username = request_data['username']
        password = request_data['password']
        friend = []
        ret, nickname, password = self.check_user_login(username, password)
        # 防止用户重复登录
        if username in self.clients.keys():
            ret, nickname, password = '-2', '', username

        # 判断是否登录成功
        if ret == '1':
            self.clients[username] = {"sock": client_soc, "nickname": nickname}
            friends = self.select_user_friends(username)

            # 处理反回的信息
            response_text = ResponseProtocol.response_login_result(ret, nickname, username, friends)
            # 把信息发送给用户
            client_soc.send_data(response_text)

            return
        # 处理反回的信息
        response_text = ResponseProtocol.response_login_result(ret, nickname, username, friend)
        # 把信息发送给用户
        client_soc.send_data(response_text)
    def request_chat(self,soc,request_data):
        # 处理聊天请求
        print(request_data)
        message = request_data['messages']
        username = request_data['username']
        to_user = request_data['to_user']

        nickname = self.clients[username]['nickname']

        # 拼接发送的字符串
        msg = ResponseProtocol.response_chat(nickname,username,message,to_user)

        # 把字符串发送给所有人
        if to_user == 'ALL':
            for u_name,info in self.clients.items():
                if username == u_name:
                    continue
                info['sock'].send_data(msg)
                # 向其他所有在线用户发送消息

        else:
            for u_name,info in self.clients.items():
                if u_name == to_user:
                    print(f'to_user: {to_user}')
                    self.clients[u_name]['sock'].send_data(msg)



    def request_register(self,client_soc,request_data):
        username = request_data['username']
        password = request_data['password']
        nickname = request_data['nickname']
        ret, username, password, nickname = self.check_user_register(username, password, nickname)
        # 处理反回的信息
        response_text = ResponseProtocol.response_regist(ret, username, password, nickname)
        # 把信息发送给用户
        client_soc.send_data(response_text)
    def request_change(self,client_soc,request_data):
        username = request_data['username']
        other = request_data['other']
        result, username, other, other_username = self.check_user_change(username, other)
        # 处理反回的信息
        response_text = ResponseProtocol.response_change(result, username, other, other_username)
        print(f'更换角色{response_text}')
        # 把信息发送给用户
        client_soc.send_data(response_text)
    def select_user_friends(self,username):
        sql = "SELECT f.F_Name AS FriendNickName, u2.U_LoginID AS FriendLoginID FROM user u1 JOIN friends f ON u1.U_ID = f.F_UserID JOIN user u2 ON f.F_FriendID = u2.U_ID WHERE u1.U_LoginID = %s; "
        result = self.db.select(sql, data= username)
        print(result)
        print(type(result))
        for index, username in enumerate(result):
            print(username['FriendNickName'])
            print(username['FriendLoginID'])

        return result

    def check_user_login(self, username, password):

        sql ="select * from user where U_LoginID=%s and U_Password=%s;"
        result = self.db.select(sql, (username, password))
        # 没找到，用户不存在
        if not result:
            return '0','',username
        # 密码错误
        if password != result[0]['U_PassWord']:
            return '-1','',username
        return '1',result[0]['U_NickName'],username
    def check_user_register(self, username, password, nickname):

        sql = "SELECT * FROM user WHERE U_LoginID = %s AND U_PassWord = %s;"
        result = self.db.select(sql,(username,password))
        if not result:
            # 待插入
            sql = f"INSERT INTO user (U_LoginID, U_PassWord, U_NickName, U_UserStateID)VALUES (%s, %s, %s, 1);"

            result= self.db.insert(sql, (username, password, nickname))
            return result, username, password, nickname
        else:
            return '0', '', '', ''

    def check_user_change(self, username, other):
        for u_name,info in self.clients.items():

            if other == info['nickname']:

                return '1',username,other,u_name

        return '0',username,other,'error'


if __name__ == '__main__':
    s=Server()
    s.startup()
