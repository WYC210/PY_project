from Request_Protocol import RequestProtocol
from tkinter.messagebox import showinfo
from client_socket import ClientSocket
from window_regist import WindowRegist
from window_login import WindowLogin
from window_chat import WindowChat
from datetime import datetime
from windwo_music import *
from threading import Thread
from config import *
import queue
import sys

class Client(object):
    def __init__(self):
        # 初始化登录界面
        self.window = WindowLogin()
        # 初始化注册界面
        self.register = WindowRegist()
        # 初始化聊天窗口
        self.chat = WindowChat()
        # 设置聊天LOGO
        self.window.iconbitmap(r'D:\code\chat\img\1.ico')
        # 先把聊天窗口隐藏
        self.chat.withdraw()
        # 把注册窗口隐藏
        self.register.withdraw()
        # 初始化音乐播放器
        self.player = MusicPlayer()

        # 播放音乐文件
        self.player.play_music("123.mp3")
        # 初始化消息队列，用于调度主线程中的 UI 更新
        self.ui_update_queue = queue.Queue()

        # 初始化登录重置点击
        self.window.on_reset_button_clicked(self.clear_window_input)
        self.window.on_login_button_clicked(self.send_window_login_data)
        self.window.on_enroll_button_clicked(self.create_window_user)
        self.window.on_window_close(self.exit_window)

        # 初始化注册点击
        self.register.on_reset_button_clicked(self.clear_register_input)
        self.register.on_enroll_button_clicked(self.create_register_user)
        self.register.on_back_button_clicked(self.back_register_user)
        self.register.on_register_close(self.exit_window)

        # 聊天窗口发送按钮点击事件
        self.chat.on_send_button_clicked(self.send_chat_data)
        self.chat.on_change_button_clicked(self.send_change_chat)
        self.chat.on_add_button_click(self.add_friend)
        self.chat.on_del_button_click(self.del_friend)
        self.chat.on_music_button_click(self.music)
        self.chat.on_window_close(self.exit_window)
        self.chat.on_stop_music_button_click(self.stop_music)

        # 初始化客户端消息处理函数
        self.response_handle_fun = {}
        self.regist(RESPONSE_LOGIN_RESULT, self.response_login_handle)
        self.regist(RESPONSE_CHAT, self.response_chat_handle)
        self.regist(RESPONSE_REGISTER, self.response_register_handle)
        self.regist(RESPONSE_CHANGE,self.response_change_handle)

        # 在线用户名
        self.username = None
        # 存储切换昵称
        # 存储双向聊天记录
        self.chat_records = dict()

        # 存储用户切换聊天人
        self.change_user = dict()
        # 创建客户端套接字
        self.conn = ClientSocket()
        self.response_data = None
        # 程序是否在运行
        self.runing = True

    def regist(self, request_id, fun):
        # 注册信息和处理信息对应的方法到字典
        self.response_handle_fun[request_id] = fun

    def startup(self):
        # 链接服务器
        self.conn.connect()

        # 创建子线程，不断接收消息
        Thread(target=self.response_handle).start()

        # 开启窗口
        self.window.mainloop()

    def clear_window_input(self):
        # 清理输入框
        self.window.clear_username()
        self.window.clear_password()

    def send_window_login_data(self):
        # 获取账号密码
        username = self.window.get_username()
        password = self.window.get_password()

        # 生成文本协议
        request_text = RequestProtocol.response_login_result(username, password)

        self.conn.send_data(request_text)

    def create_window_user(self):
        # 进行账号注册
        # 显示注册窗口
        self.register.update()
        self.register.deiconify()
        # 隐藏登陆窗口
        self.window.withdraw()

    def send_chat_data(self,):
        # 获取输入内容到服务器
        message = self.chat.get_input()
        nickname = self.response_data['nickname']
        to_use = self.response_data['to_user']
        # 点击发送清空聊天框内容
        self.chat.clear_input()
        # 拼接协议
        request_text = RequestProtocol.request_chat(nickname,self.username, message,to_use)
        # 发送消息
        self.conn.send_data(request_text)

        # 把发送的消息传到聊天区
        self.chat.append_message('我', message)

    def response_handle(self):
        # 接收服务器消息
        while self.runing:
            # 接收数据
            recv_data = self.conn.recv_data()

            # 解析数据
            response_data = self.parse_response_data(recv_data)
            print('解析完')
            print(response_data)

            handle_fun = self.response_handle_fun[response_data['response_id']]

            if handle_fun:
                handle_fun(response_data)

            # 每次处理后检查并处理 UI 更新任务
            self.window.after(0, self.process_ui_updates)

    def parse_response_data(self, recv_data):
        # 解析响应数据
        response_data_list = recv_data.split(DELIMITER)
        response_data = dict()
        response_data['response_id'] = response_data_list[0]

        if response_data['response_id'] == RESPONSE_LOGIN_RESULT:
            response_data['result'] = response_data_list[1]
            response_data['nickname'] = response_data_list[2]
            response_data['username'] = response_data_list[3]
            response_data['friend'] = response_data_list[4]
            response_data['to_user'] = 'ALL'
            self.response_data = response_data
        elif response_data['response_id'] == RESPONSE_CHAT:
            response_data['nickname'] = response_data_list[1]
            response_data['username'] = response_data_list[2]
            response_data['message'] = response_data_list[3]
            response_data['to_user'] = response_data_list[4]

        elif response_data['response_id'] == RESPONSE_REGISTER:
            response_data['result'] = response_data_list[1]
            response_data['username'] = response_data_list[2]
            response_data['password'] = response_data_list[3]
            response_data['nickname'] = response_data_list[4]
        elif response_data['response_id'] == RESPONSE_CHANGE:
            print(response_data)
            response_data['result'] = response_data_list[1]
            response_data['username'] = response_data_list[2]
            response_data['to_nickname'] = response_data_list[3]
            response_data['to_user'] = response_data_list[4]
        return response_data

    def response_login_handle(self, response_data):
        # 登录结果响应
        if response_data['result'] == '0':
            showinfo('提示', "登陆失败,未查到该用户信息!")
            return
        elif response_data['result'] == '-1':
            showinfo('提示', "登陆失败,账号或密码错误!")
            return
        elif response_data['result'] == '-2':
            showinfo('提示', "登陆失败,请不要重复登陆!")
            return
        showinfo('提示', "登陆成功!")
        nickname = response_data['nickname']
        self.username = response_data['username']
        friends = response_data['friend']
        # 获取到的好友信息添加到字典里
        self.chat.post_friends(friends)
        # 从字典里读取信息渲染
        self.chat.set_friends()
        # 登录成功显示聊天窗口
        self.chat.title(nickname)
        self.chat.update()
        self.chat.deiconify()
        # 隐藏登录窗口
        self.window.withdraw()

    def response_chat_handle(self, response_data):
        sender_nick_name = response_data['nickname']  # 消息发送者昵称
        message = response_data['message']  # 消息内容
        to_user = response_data['to_user']  # 消息目标用户
        username = response_data['username']  # 消息发送者的用户名
        self_user = self.username  # 当前用户
        self_to_user = self.chat.get_select_user()
        print("大胆")
        print(f'发送人昵称{sender_nick_name}，消息{message}，发给{to_user}，发送人ID{username}，自己ID{self_user}，自己在跟谁聊天{self_to_user}')
        if self_to_user == 'main_group':
            self_to_user = 'ALL'
        # 确保聊天记录的键是固定顺序（双向存储）
        key = tuple(sorted([to_user, username]))

        if key not in self.chat_records:
            self.chat_records[key] = []  # 初始化聊天记录

        # 创建消息记录
        message_entry = {
            'sender': username,
            'receiver': to_user,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # 存储消息
        self.chat_records[key].append(message_entry)
        print(self.chat_records)
        # 如果目标用户是当前聊天用户，则立即显示消息
        if to_user == 'ALL' and to_user == self_to_user:
            display_name = "我" if username == self_user else sender_nick_name
            self.chat.append_message(f"{display_name}", message)
        else:
            self.chat.update_unread(username, 1)
        # 私聊
        if to_user != 'ALL' and sender_nick_name == self_to_user:
            self.chat.append_message(f"{sender_nick_name}", message)

    def response_register_handle(self, response_data):
        if response_data['result'] == '0':
            showinfo('提示', "注册失败，已存在相同的用户信息!")
            return
        showinfo('提示', "注册成功!")
        # 注册成功后显示登录窗口
        self.window.update()
        self.window.deiconify()

        # 将注册窗口操作放入队列，在主线程中执行
        self.ui_update_queue.put(self.register.withdraw)

    def exit_window(self):
        self.runing = False
        self.player.stop_music()
        self.conn.close()
        sys.exit(0)
    def clear_register_input(self):
        self.register.clear_username()
        self.register.clear_password()
        self.register.clear_nickname()

    def create_register_user(self):
        username = self.register.get_username()
        password = self.register.get_password()
        nickname = self.register.get_nickname()

        # 生成文本协议
        request_text = RequestProtocol.request_regist(username, password, nickname)
        self.conn.send_data(request_text)
        print('发送注册信息')

    def process_ui_updates(self):
        # 处理 UI 更新队列中的所有任务
        while not self.ui_update_queue.empty():
            update_task = self.ui_update_queue.get()
            update_task()  # 执行更新任务

    def back_register_user(self):
        self.window.update()
        self.window.deiconify()
        self.register.withdraw()

    def send_change_chat(self):
        # 获取选择的聊天用户
        user = self.chat.get_select_user().strip('`')  # 获取当前选中用户

        if not user:
            return

        if user == 'main_group':  # 切换到群聊
            self.chat.clear_chat()
            self.chat.append_message("系统消息 :", '切换成功')
            self.response_data['to_user'] = 'ALL'
            return
        print(f"切换的用户是{user}")
        # 发送切换聊天目标请求到服务器
        request_text = RequestProtocol.request_change(self.username, user)
        self.conn.send_data(request_text)
    def response_change_handle(self, response_data):
        result = response_data['result']  # 切换结果
        self_user = response_data['username']  # 当前用户
        to_user = response_data['to_user']  # 切换的目标用户
        to_nickname = response_data['to_nickname']

        if result == '0':
            showinfo('提示', "切换失败，目前只支持切换在线用户!")
            return

        # 切换成功，清空聊天窗口
        self.chat.clear_chat()
        self.chat.append_message("系统消息:", "切换成功")
        self.response_data['to_user'] = to_user

        # 确保聊天记录的键是固定顺序（双向存储）
        key = tuple(sorted([self_user, to_user]))
        print('6666666666666666666')
        print(self_user)
        print(to_user)
        print(to_nickname)
        print(key)
        print(self.chat_records)

        # 加载与目标用户的所有聊天记录
        if key in self.chat_records:
            chat_history = self.chat_records[key]
            for record in chat_history:
                sender = record['sender']
                message = record['message']
                timestamp = record['timestamp']
                display_name = "我" if sender == self_user else to_nickname
                self.chat.append_message(display_name, message,timestamp)
            self.chat.update_unread(to_user, -1)
    def add_friend(self):
        friend_ = self.chat.get_select_friend_input()


    def del_friend(self):
        pass

    def music(self):
        pass

    def stop_music(self):
        self.player.stop_music()


s = Client()
s.startup()

