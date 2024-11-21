import asyncio
# # 初始化
# a = 0
# b = 0
# c = 1
# d = 1
#
# e = 2
# f = 2
# g = 10
# h = 10
#
# #----------------------------------------
# a = a + 1
# print(a)
# b += 1 # b = b + 1
# print(b)
#
# c = c - 1
# print(c)
# d -= 1
# print(d)
# e = e * 2
# print(e)
# e *= 2
# print(e)
# g = g / 2
# print(g)
# h /= 2
# print(h)

# range(6) #0-?
# range(1,6) # 1-?
# 1 - 100 求和
# sum = 0  # 1+2+3+4+5+6+...100
# for num in range(1,101):
#     print(f'第{num}次循环 {sum} ={sum} + {num}  ')
#     sum = sum + num
#     break

# print("退出")
    # print(f'第{num}次循环num = {num}') # 被执行了100遍 1,2,3,4,5,....100

#循环
# a = 0  # 1 1+1 =2  2+ 1 =3 ...... 10
# while( a < 10): # False
#     a += 1
#     print(a)
#增删改查
a = [] # 列表
sda = [1,2,3,4,5]
# 插入
# a.insert(3,3.5)
# a.append(6)
#删 【1，2，3，4】

# a.pop()

# del a

# a.remove(2)
# a.clear()

# a[2] =6
# print(a)
# print(a.index(3))
# b = a.index(3)
# a[b] = 6
# print(a)
# print(len(a))



#把李鑫改成张鑫，查找’10072的下标,在小明前面添加一个黑奴李鑫，删除除‘10072’
# a = [10086,'10072','小明','李鑫',10072]
#        键：     值
# a = {'name':"李鑫",'year': '3'}
#
# b = a.pop('year')
#
# for i in a.keys():
#     print(i)
#

#                     ===============编程思想=================

# 1. 开始

# 输入员工全年累计应纳所得税
# money =eval(input("输入累计应纳所得额"))
# # 初始化参数
# tax_7 = tax_6 = tax_5 = tax_4 = tax_3 = tax_2 = tax_1 = 0
# # x - 员工全年累计应纳所得额
# if money > 960000:
#     tax = money - 960000  # # 超过960000
#     tax_7 = tax * 0.45 - 181920
# elif money > 660000 and money < 960000:  #超过660000
#     tax = money - 660000
#     tax_6 = tax * 0.35 - 85920
# elif money < 420000 and money > 660000: #超过420000
#     tax = money - 42000078
#     tax_5 = tax * 0.3 - 52920
# elif money < 300000 and money > 420000: #超过300000
#     tax = money - 300000
#     tax_4 = tax * 0.25 - 31920
# elif money < 144000 and money > 300000: #超过144000
#     tax = money - 144000
#     tax_3 = tax * 0.2 - 16920
# elif money < 360000 and money > 144000: #超过36000
#     tax = money - 360000
#     tax_2 = tax * 0.1 - 2520
# else : # 不超过36000
#     tax_1 = money * 0.3
# # 应缴纳税额的总和
# tax_sum = tax_7 + tax_6 + tax_5 + tax_4 + tax_3 + tax_2 + tax_1
# print(f"你需要缴纳{tax_sum}元")
#
#
#
async def func01():
    print(1)
    await asyncio.sleep(3)
    print(2)


async def func02():
    print(3)
    await asyncio.sleep(3)
    print(4)


async def func03():
    print(5)
    await asyncio.sleep(3)
    print(6)


async def main():
    f1 = asyncio.create_task(func01())
    f2 = asyncio.create_task(func02())
    f3 = asyncio.create_task(func03())

    await asyncio.gather(f1, f2, f3)


# 使用 asyncio.run() 来运行主异步函数
# asyncio.run(main())
# import requests
# import pandas as pd
#
# def GetTable(url):
#     header = {
#         'Cookie':'username=rzgc'
#     }
#     response = requests.get(url=url,headers = header)
#
#     html = pd.read_html(response.text)
#     table = html[0]
# f
#
#     table.drop(columns=['报告期  单季度'], inplace=True,errors='ignore',x)
#
#     table.drop(columns=['报告期  单季度.1'], inplace=True,errors='ignore')
#     financial =table
#     financial =financial.replace('-',0)
#     return financial
# 'http://fz.chinaive.com/rzcj/SH600176/ZCFZB.html'
# url='http://fz.chinaive.com/rzcj/{}/ZCFZB.html'.format('SH600176')
# print(url)
# print(GetTable(url))
#  1. 导入模块
#  1. 导入模块
import requests
import os
import pandas as pd
import time


# 2.  打开要爬取的企业股票代码，根据 TXT文档进行正则后处理，获取到代码编号
def StockDict(stock, name):
    """
    用于生成 股票代码 对应 公司名称 的字典数据
    :param stock: 股票代码列表数据
    :param name: 公司名称列表数据
    :return:字典
    """
    stock_dict = dict(zip(stock, name))
    return stock_dict


# 3. 从 HTML 中获取表单数据
def getTable(stockIndex, url):
    """
    获取 HTML 中的 table 表格型数据
    :param stockIndex: 股票代码TXT文档中的代码元素
    :param url:目标网站url
    :return:获取到的财务报表
    """
    header = {
        'Cookie': 'username=rzgc'
    }
    response = requests.get(url.format(stockIndex), headers=header)
    response.encoding = 'utf-8'
    table = pd.read_html(response.text)
    return table


# 4. 将表单数据写入 excel
def df2excel(df, xlsx_name, sheet_name):
    """
    将 dataframe 格式的数据写入到表格中
    :param df: 存有数据的dataframe
    :param xlsx_name: 需要写入的xlsx文件的名称
    :param sheet_name: 需要写入的sheet名
    :return: None
    """
    file_path = r'C://rzgc/data/python/'
    file_paths = r'C://rzgc/data/path/'

    with pd.ExcelWriter(xlsx_name, mode='w', engine='openpyxl') as witer:
        df.to_excel(witer, sheet_name=sheet_name, index=False)

    with pd.ExcelWriter(xlsx_name, mode='w', engine='openpyxl') as witer:
        df.to_excel(witer, sheet_name=sheet_name, index=False)


# 5. 遍历股票代码，循环执行步骤 （3.从 HTML 中获取表单数据） 获取网页中的表单数据，并显示进度
def main():
    """
    遍历股票代码，获取全部财务报表
    :return: None
    """
    stock = ['SH600176', 'SH600425', 'SH600720', 'SH601992', 'SH603737', 'SH605318', 'SZ000055', 'SZ002043', 'SZ002271',
             'SZ002372']
    name = ['中国巨石', '青松建化', '祁连山', '金隅集团', '三棵树', '法狮龙', '方大集团', '兔宝宝', '东方雨虹',
            '伟星新材']
    stockDict = StockDict(stock, name)
    #  遍历股票代码字典，输出当前正在读取的股票代码进行进度的展示
    for key, value in stockDict.items():
        time.sleep(0.1)
        print("正在读取股票代码：%s" % key)
        #  遍历资产负债表和利润表两个网页的 url 字典，输出当前正在写入的表单为哪个财务报表进行进度的展示
        balance_sheet_url = r'http://fz.chinaive.com/rzcj/{}/ZCFZB.html'.format(key)
        income_statement = r'http://fz.chinaive.com/rzcj/{}/GSLRB.html'.format(key)
        path = r'C://rzgc/data/python/'
        balance_df = getTable(key, balance_sheet_url)
        if balance_df:
            df2excel(balance_df[0], path + value + '.xlsx', value)
        income_df = getTable(key, income_statement)
        if income_df:
            df2excel(income_df[0], path + value + '.xlsx', value)


main()