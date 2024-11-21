from tkinter import Tk, Label, Entry, Frame, Button,END
class WindowRegist(Tk):
    def __init__(self):
        super(WindowRegist,self).__init__()

        # 设置窗口属性
        self.window_init()
        # 填充控件
        self.add_widgets()

    def window_init(self):
        # 初始化窗口
        window_width = 280
        window_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = int((screen_width / 2) - (window_width / 2))
        pos_y = int((screen_height / 2) - (window_height / 2))
        # 设置窗口不能被拉伸
        self.resizable(False, False)
        # 设置窗口标题
        self.title("注册窗口")
        # 设置窗口大小和位置
        self.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    def add_widgets(self):
        # 给窗口添加组件
        logo_label = Label(self)
        logo_label['text'] = '成为微聊的一员 !'
        logo_label.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=20, pady=20)  # 跨两列，并填充整个单元格


        user_label = Label(self)
        user_label['text'] = '用户名:'
        user_label.grid(row=1, column=0, padx=5, pady=5)

        user_entry = Entry(self, name='user_entry')
        user_entry['width'] = 25
        user_entry.grid(row=1, column=1, padx=10, pady=5)

        password_label = Label(self)
        password_label['text'] = '密  码:'
        password_label.grid(row=2, column=0, padx=10, pady=10)

        password_entry = Entry(self, name='password_entry')
        password_entry['width'] = 25
        password_entry['show'] = '?'
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        nick_label = Label(self)
        nick_label['text'] = '昵  称:'
        nick_label.grid(row=3, column=0, padx=10, pady=10)

        nick_entry = Entry(self, name='nick_entry')
        nick_entry['width'] = 25

        nick_entry.grid(row=3, column=1, padx=10, pady=10)

        nick_label = Label(self)
        nick_label['text'] = '性  别:'
        nick_label.grid(row=4, column=0, padx=10, pady=10)

        nick_entry = Entry(self, name='sex_entry')
        nick_entry['width'] = 25

        nick_entry.grid(row=4, column=1, padx=10, pady=10)



        age_label = Label(self)
        age_label['text'] = '年  龄:'
        age_label.grid(row=5, column=0, padx=10, pady=10)

        age_entry = Entry(self, name='age_entry')
        age_entry['width'] = 25
        age_entry.grid(row=5, column=1, padx=10, pady=10)

        button_frame = Frame(self, name='button_frame')

        back_button = Button(button_frame, name='back_button')
        back_button['text'] = ' 返回 '
        back_button.pack(side='left', padx=15)

        reset_button = Button(button_frame, name='reset_button')
        reset_button['text'] = ' 重置 '
        reset_button.pack(side='left', padx=15)

        enroll_button = Button(button_frame, name='enroll_button')
        enroll_button['text'] = ' 注册 '
        enroll_button.pack(side='right', padx=15)

        button_frame.grid(row=6, columnspan=2, padx=5, pady=5)
    def clear_username(self):
        self.children['user_entry'].delete(0,END)
    def clear_password(self):
        # 清除密码内容
        self.children['password_entry'].delete(0, END)
    def clear_nickname(self):
        self.children['nick_entry'].delete(0,END)

    def get_username(self):
        return self.children['user_entry'].get()
    def get_password(self):
        return self.children['password_entry'].get()
    def get_nickname(self):
        return self.children['nick_entry'].get()

    def on_back_button_clicked(self, command):
        # 处理重制按钮
        back_button = self.children['button_frame'].children['back_button']
        back_button['command'] = command

    def on_reset_button_clicked(self,command):
        # 处理重制按钮
        reset_button = self.children['button_frame'].children['reset_button']
        reset_button['command'] = command

    def on_enroll_button_clicked(self,command):
        # 处理注册
        enroll_button = self.children['button_frame'].children['enroll_button']
        enroll_button['command']=command
    def on_register_close(self,command):
        # 窗口关闭
        self.protocol('WM_DELETE_WINDOW',command)
if __name__ == '__main__':
    window = WindowRegist()
    window.mainloop()


