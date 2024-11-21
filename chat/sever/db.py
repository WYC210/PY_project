from pymysql import connect
from config import *

class DB:
    def __init__(self):
        # 链接数据库
        self.conn = connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, database=DB_NAME, charset='utf8')
        # 获取游标
        self.cursor = self.conn.cursor()


    def select(self, sql,data=None):
        # 进行查询
        self.cursor.execute(sql,data)
        # 查询结果
        results = self.cursor.fetchall()
        if not results:
            return None
        # 获得字段列表
        fields = [field[0] for field in self.cursor.description]
        # 使用列表的列表来存储所有行的数据
        data = []
        for row in results:
            row_data = dict(zip(fields, row))  # 将每一行的数据转换为字典
            data.append(row_data)  # 将字典添加到列表中
        return data
    def insert(self, sql,data):

        self.cursor.execute(sql,data)
        # 提交数据
        self.conn.commit()
        return '1'

    def close(self):
        # 关闭数据库
        self.cursor.close()
        self.conn.close()
# if __name__ == '__main__':
#     db = DB()
#     id = input("1")
#     pw = input("2")
#     sql = 'select * from user where U_LoginID = "%s" && U_PassWord = "%s"' % (id, pw)
#     print(sql)
#     a=db.select(sql)
#     print(a[0])
#     print(a[1])
#     print(a[2])