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
        self.friends = ["Alice", "Bob", "Charlie", "David", "Eve"]
        self.groups = ["main_group"]
        self.selected_user = None  # 当前选择的聊天对象
        self.friends_dict = {user: 1 for user in self.friends + self.groups}  # 未读消息计数
        print(self.friends_dict)
        # 切换按钮的回调函数
        self.change_button_callback = None

        # 添加界面组件
        self.add_widget()

    def add_widget(self):
        # 主容器
        main_frame = Frame(self)
        main_frame.pack(fill="both", expand=True)
        self.children['main_frame'] = main_frame

        # 左侧好友/群聊列表区域
        self.user_list_frame = Frame(main_frame, width=200)
        self.user_list_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.children['user_list_frame'] = self.user_list_frame

        Label(self.user_list_frame, text="在线好友和群聊", font=("Arial", 14)).pack(pady=10)

        # 创建好友列表
        self.listbox = Listbox(self.user_list_frame, width=30, height=20)
        self.listbox.pack(side="left", padx=10, pady=5)
        self.children['listbox'] = self.listbox

        scrollbar = Scrollbar(self.user_list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.children['scrollbar'] = scrollbar

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # 将好友和群聊添加到 Listbox
        self.update_friend_list()

        # 绑定双击事件到 change_button 的回调
        self.listbox.bind("<Double-1>", self.trigger_change_button)

        # 右侧聊天区
        chat_frame = Frame(main_frame)
        chat_frame.pack(side="right", fill="both", expand=True)
        self.children['chat_frame'] = chat_frame

        # 聊天区
        self.chat_text_area = ScrolledText(chat_frame, width=90, height=28)
        self.chat_text_area.pack(padx=10, pady=10)
        self.chat_text_area.config(state='disabled')
        self.children['chat_text_area'] = self.chat_text_area

    def update_friend_list(self):
        """
        更新好友列表，显示未读消息数。
        """
        self.listbox.delete(0, END)
        for user, unread_count in self.friends_dict.items():
            if unread_count > 0:
                display_name = f"{user} ({unread_count}条未读)"
            else:
                display_name = user
            self.listbox.insert(END, display_name)

    def add_unread_message(self, user):
        """
        增加指定用户的未读消息数。
        """
        if user in self.friends_dict and user != self.selected_user:
            self.friends_dict[user] += 1
            self.update_friend_list()

    def clear_unread_message(self, user):
        """
        清除指定用户的未读消息数。
        """
        if user in self.friends_dict:
            self.friends_dict[user] = 0
            self.update_friend_list()

    def trigger_change_button(self, event=None):
        """
        在双击列表项或点击按钮时触发切换按钮的回调函数。
        """
        selected_index = self.listbox.curselection()
        if selected_index:
            self.selected_user = self.listbox.get(selected_index).split(" ")[0]  # 获取用户名称
            self.set_title()
            self.clear_unread_message(self.selected_user)
            if self.change_button_callback:
                self.change_button_callback()

    def receive_message(self, user, message):
        """
        模拟收到一条新消息。
        """

        self.add_unread_message(user)

    def set_title(self):
        if self.selected_user:
            self.title(f"与 {self.selected_user} 聊天中")

    def append_message(self, user, message):
        """
        添加消息到聊天区。
        """
        self.children['chat_text_area'].config(state='normal')
        send_time = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
        sendinfo = f"{user}: {send_time}\n"
        self.children['chat_text_area'].insert(END, sendinfo, 'green')
        self.children['chat_text_area'].insert(END, f"    {message}\n")
        self.children['chat_text_area'].yview(END)
        self.children['chat_text_area'].config(state='disabled')




if __name__ == "__main__":
    app = WindowChat()

    # 模拟消息接收
    def simulate_receive_message():
        import random
        user = random.choice(app.friends)
        app.receive_message(user, "这是一条新消息！")

    app.after(3000, simulate_receive_message)  # 每3秒模拟一次消息接收
    app.mainloop()
