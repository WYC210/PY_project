import asyncio

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
