from tkinter.scrolledtext import ScrolledText
from time import localtime, strftime, time
from tkinter.ttk import Combobox
from tkinter import *

class WindowChat(Toplevel):
    def __init__(self):
        super(WindowChat, self).__init__()
        self.title("聊天系统")
        self.geometry("950x500")
        self.resizable(False, False)

        # 初始化一些变量
        # 好友列表
        self.friends = list()
        # 群聊列表
        self.groups = ["main_group"]
        # 存储好友的username : nickname
        self.friends_dict = dict()

        self.selected_user = None  # 当前选择的聊天对象

        # 切换按钮的回调函数
        self.change_button_callback = None

        # 添加界面组件
        self.add_widget()
        # 记录当前聊天人
        self.to_user = 'ALL'

    def add_widget(self):
        # 创建主容器
        main_frame = Frame(self,bg='#F1E9D2')
        main_frame.pack(fill="both", expand=True)
        self.children['main_frame'] = main_frame

        # 左侧好友/群聊列表区域
        self.user_list_frame = Frame(main_frame, width=200,bg='#F1E9D2')
        self.user_list_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.children['user_list_frame'] = self.user_list_frame


        mini_frame = Frame(main_frame, width=200,bg='#F1E9D2')
        mini_frame.pack(side="top", fill="y")
        Label(self.user_list_frame, text="在线好友和群聊", font=("Arial", 14),bg='#F1E9D2').pack(pady=10)
        # 切换聊天音乐
        Music_button = Button(self.user_list_frame,  width=8, height=1,text= '切换音乐(未实现)')
        Music_button.pack(side="top", padx=3)
        self.children['music_button'] = Music_button

        self.entry =Entry(mini_frame,width=10)
        self.entry.pack(side="left", fill="x")



        # 添加好油
        add_button = Button(mini_frame, text='添加好友(未实现)', width=8, height=1, command=self.trigger_change_button)
        add_button.pack(side="left", padx=3)
        self.children['add_button'] = add_button

        # 删除好友
        del_button = Button(mini_frame, text='删除好友(未实现)', width=8, height=1)
        del_button.pack(side="right", padx=3)
        self.children['del_button'] = del_button

        # 更换背景
        stop_music_button = Button(mini_frame, text='暂停音乐', width=8, height=1)
        stop_music_button.pack(side="right", padx=3)
        self.children['stop_music_button'] = stop_music_button


        # 创建好友列表
        self.listbox = Listbox(self.user_list_frame, width=30, height=20,bg='#F1E9D2')
        self.listbox.pack(side="left", padx=10, pady=5)
        self.children['listbox'] = self.listbox

        scrollbar = Scrollbar(self.user_list_frame, orient="vertical",bg='#F1E9D2')
        scrollbar.pack(side="right", fill="y")
        self.children['scrollbar'] = scrollbar

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)



        # 绑定双击事件到 change_button 的回调
        self.listbox.bind("<Double-1>", self.trigger_change_button)

        # 右侧聊天区
        chat_frame = Frame(main_frame,bg='#F1E9D2')
        chat_frame.pack(side="right", fill="both", expand=True)
        self.children['chat_frame'] = chat_frame

        # 聊天区 - 增加高度，让聊天区变长
        self.chat_text_area = ScrolledText(chat_frame, width=90, height=28,bg='#F1E9D2')  # 增加高度为25
        self.chat_text_area.pack(padx=10, pady=10)
        self.chat_text_area.config(state='disabled')
        self.children['chat_text_area'] = self.chat_text_area

        # 输入框和发送按钮
        input_frame = Frame(chat_frame,bg='#F1E9D2')
        input_frame.pack(padx=10, pady=5, fill="x")

        self.children['input_frame'] = input_frame

        # 调整输入框的宽度
        self.chat_input_area = ScrolledText(input_frame, width=50, height=3,bg='#F1E9D2')  # 将宽度调整为50
        self.chat_input_area.pack(side="left", fill="both", expand=True)
        self.children['chat_input_area'] = self.chat_input_area

        send_button = Button(input_frame, text='发送', width=5, height=2,bg='#F1E9D2')
        send_button.pack(side="right", padx=5)
        self.children['send_button'] = send_button

    def get_input(self):
        # 获取输入框内容
        return self.children['chat_input_area'].get(0.0, END)  # 参数必须是浮点数

    def clear_input(self):
        self.children['chat_input_area'].delete(0.0, END)  # 参数必须是浮点数


    def on_send_button_clicked(self, command):
        # 当发送按钮被点击
        self.children['send_button']['command'] = command

    def get_select_user(self):
        """
        获取选择的用户或群聊。如果没有选择任何用户，返回 'ALL'。
        """
        selected_index = self.listbox.curselection()  # 获取当前选中项的索引
        if selected_index:
            # 获取选中项的文本
            selected_text = self.listbox.get(selected_index[0])

            # 处理显示格式：提取用户名（去掉括号内的附加信息）
            self.selected_user = selected_text.split(" ")[0]  # 默认取空格前的第一个部分

            # 更新窗口标题
            self.set_title()
            self.to_user = self.selected_user
            return self.selected_user
        else:
            # 没有选中任何用户时返回上次记录的值
            return self.to_user
    def on_stop_music_button_click(self,command):
        self.children['stop_music_button']['command'] = command   
    def get_select_friend_input(self):
        return self.entry.get(0.0, END)  # 参数必须是浮点数
    def on_add_button_click(self, command):
        # 当发送按钮被点击
        self.children['add_button']['command'] = command
    def on_del_button_click(self, command):
        # 当发送按钮被点击
        self.children['del_button']['command'] = command
    def on_music_button_click(self, command):
        # 当发送按钮被点击
        self.children['music_button']['command'] = command
    def set_title(self):
        if self.selected_user:
            self.title(f"与 {self.selected_user} 聊天中")

    def on_window_close(self, command):
        # 当窗口关闭执行
        self.protocol('WM_DELETE_WINDOW', command)

    def append_message(self, user, message,send_time = None):
        # 先将聊天区设置为可编辑状态
        self.children['chat_text_area'].config(state='normal')
        if not send_time :
            # 添加消息到聊天区
            send_time = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
        sendinfo = f' {user}: {send_time} \n'
        self.children['chat_text_area'].insert(END, sendinfo, 'green')  # 发送人信息
        self.children['chat_text_area'].insert(END, '    ' + message + '\n')
        # 向下滚动屏幕
        self.children['chat_text_area'].yview_scroll(3, UNITS)
        # 再次禁用编辑
        self.children['chat_text_area'].config(state='disabled')

    def clear_chat(self):
        # 将聊天区设置为可编辑状态
        self.children['chat_text_area'].config(state='normal')

        # 清空聊天内容
        self.children['chat_text_area'].delete(1.0, END)

        # 再次禁用编辑
        self.children['chat_text_area'].config(state='disabled')

    def set_friends(self):
        lists = list()
        # 将好友和群聊添加到 Listbox
        for i in self.friends:
            if i in self.friends_dict:
                lists.append(self.friends_dict[i])

        for user in lists + self.groups:
            self.listbox.insert(END, user)



    def on_change_button_clicked(self, command):
        """
        设置切换按钮的回调函数。
        """
        self.change_button_callback = command
    def post_friends(self,friends):
        # 将 Bob:user2;Charlie:user3 转换回字典列表
        friends_list = [
            {"FriendNickName": pair.split(":")[0], "FriendLoginID": pair.split(":")[1]}
            for pair in friends.split(";")
        ]
        # 更新好友列表
        for value in friends_list:  # 遍历字典列表
            self.friends_dict[value['FriendLoginID']] = value['FriendNickName']
            self.friends.append(value['FriendLoginID'])

    def update_unread(self,username,count):
        """
        更新好友列表，显示未读消息数。
        {'Alice': 1, 'Bob': 1, 'Charlie': 1, 'David': 1, 'Eve': 1, 'main_group': 1}
        """


        # if username not in self.friends or username != '系统消息':
        #     return
        # 清空 Listbox
        self.listbox.delete(0, END)
        if count == -1:
            count = 0

        # 遍历所有好友和群聊，重新更新显示
        for friend in self.friends:
            if friend == username and count > 0:
                display_name = f"{self.friends_dict[friend]} (有未读)"
            else:
                display_name = self.friends_dict[friend]
            self.listbox.insert(END, display_name)

        # 添加群聊到列表
        for group in self.groups:
            self.listbox.insert(END, group)


    def clear_unread_message(self, username):
            """
            清除指定用户的未读消息数。
            """
            if username in self.friends_dict:
                self.update_unread(username, 0)  # 将未读消息数更新为 0
    

    def trigger_change_button(self, event=None):
        """
        在双击列表项或点击按钮时触发切换按钮的回调函数。
        """
        selected_index = self.listbox.curselection()
        if selected_index:
            # 提取选中用户的用户名（去掉未读消息数信息）
            self.selected_user = self.listbox.get(selected_index).split(" ")[0]
            self.set_title()

            # 清除该用户的未读消息数
            self.clear_unread_message(self.selected_user)

            # 触发切换回调函数（如果有）
            if self.change_button_callback:
                self.change_button_callback()


if __name__ == "__main__":
    app = WindowChat()
    app.post_friends('Bob:user2;Charlie:user3')
    app.update_unread('user2',-1)
    app.mainloop()
    #app.update_friend([{'FriendNickName': 'Bob', 'FriendLoginID': 'user2'}, {'FriendNickName': 'Charlie', 'FriendLoginID': 'user3'}])
