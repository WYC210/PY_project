from config import *

class RequestProtocol(object):
    @staticmethod
    def response_login_result(username,password):
        # 0001| 账号 | 密码
        return DELIMITER.join([REQUEST_LOGIN, username, password])

    @staticmethod
    def request_chat(nick_name, username, message, to_user):
        # 0002 | 昵称 | 账号 | 消息 | 发送人
        message = message.replace('|', '')

        return DELIMITER.join([REQUEST_CHAT, nick_name, username, message, to_user])

    @staticmethod
    def request_regist(username,password,nickname):
        # 0003 | 账号 | 密码 | 昵称
        return DELIMITER.join([REQUEST_REGISTER, username, password, nickname])

    @staticmethod
    def request_change(username,other_username):
        # 0004 | 谁 | 切换成谁
        return DELIMITER.join([REQUEST_CHANGE, username, other_username])