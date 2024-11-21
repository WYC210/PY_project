from config import *

class ResponseProtocol:
    @staticmethod
    def response_login_result(result, nickname, username, friends):
        # 将每个字典转换为字符串形式
        friend = ";".join([f"{item['FriendNickName']}:{item['FriendLoginID']}" for item in friends])
        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username, friend])
    @staticmethod
    def response_chat(nickname,username,messages,to_user):
        # 10002 | nickname | messages | touser ('ALL'则为全部)
        return DELIMITER.join([RESPONSE_CHAT, nickname, username,messages, to_user])
    @staticmethod
    def response_regist(result,username,password,nickname):
        return DELIMITER.join([RESPONSE_REGISTER, result, username, password, nickname])

    @staticmethod
    def response_change(result, username, other, other_username):
        # 10002 | nickname | messages | to_nickname  |touser ('ALL'则为全部)
        return DELIMITER.join([RESPONSE_CHANGE, result, username, other, other_username])