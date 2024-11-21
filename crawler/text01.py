import execjs
import os
import requests
from lxml import etree
import bs4
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
import json
def download():
    url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        "referer":  "https://music.163.com",
        "Cookie": "ab_jid=4dc76423b3b0e37a4226ab044b8bd8cfd9a7; ab_jid_BFESS=4dc76423b3b0e37a4226ab044b8bd8cfd9a7; BDUSS_BFESS=m13VERLaHBZQkJkeEttMnd4dmhyRFlmOEYxc0c1TUIwYlhFTFBSUDVMTkh1SmxtRUFBQUFBJCQAAAAAAQAAAAEAAABqXfQNtLvI~cvqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEcrcmZHK3Jmd; H_WISE_SIDS_BFESS=60841_60854_60887_60875; BAIDUID_BFESS=9BC5B1FC93BA6F88BD3BB77A2BC74A78:FG=1; ZFY=bt6bReJ0xr7piGR2tYhBd2luJ:BJnqE9L6Ny7:AWBa:B0Y:C; ab_bid=dfe9b8057f1bdb6b689b31f9de62bc03438f; ab_sr=1.0.1_YTRiNzZhZTBkMmQyYmJiM2Q1YzYzYzVlYTJkNGE0ODIwNzM2N2VjOTFlY2MzYzk3M2FhZGY1YmYwODk5Y2YyZDYyZjFiNWMzOTlhMDUzNDgzMDcxZWRlMjI2MzgyYmI0NDIxMWVmN2ZlMGIxYjlhMTc2OGIxMGJmOTYwZmRjNjQxYjUxOWMyZWEzN2Y4OWMyOGViZTBhNzUxMTgwOTQyYTMwYmE3NzA0MDQzMWUyZWUwYTQwNjE3MmJiMGVkZDNk",

    }
    file = open('yiyun.js','r').read()
    music = execjs.compile(file)
    # 将参数转换为 JSON 字符串
    ID =input("输入你想下载音乐的ID")

    params_seckey = music.call("asrsea_params",ID)

    with open('data.json', 'r') as file:
        datas = json.load(file)


    data ={
    "csrf_token": "",

        "params": datas["encText"],
        "encSecKey": datas["encSecKey"]

    }


    music_download = requests.post(url, data=data)

    dict = json.loads(music_download.text)
    # while(True):
    mp3_url = dict['data'][0]['url']
    #防止莫名其妙遇到none

    mp3 = requests.get(mp3_url, headers=header).content
    folder_name = "download_music"
    file_name = f'{ID}.mp3'
    os.makedirs(folder_name , exist_ok=True)
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'wb') as file:
        file.write(mp3)

#---------------------------------------------------------------------------------------------
def Batch_download(urls = "https://music.163.com/discover/toplist"):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        "referer": "https://music.163.com",
        "Cookie": "ab_jid=4dc76423b3b0e37a4226ab044b8bd8cfd9a7; ab_jid_BFESS=4dc76423b3b0e37a4226ab044b8bd8cfd9a7; BDUSS_BFESS=m13VERLaHBZQkJkeEttMnd4dmhyRFlmOEYxc0c1TUIwYlhFTFBSUDVMTkh1SmxtRUFBQUFBJCQAAAAAAQAAAAEAAABqXfQNtLvI~cvqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEcrcmZHK3Jmd; H_WISE_SIDS_BFESS=60841_60854_60887_60875; BAIDUID_BFESS=9BC5B1FC93BA6F88BD3BB77A2BC74A78:FG=1; ZFY=bt6bReJ0xr7piGR2tYhBd2luJ:BJnqE9L6Ny7:AWBa:B0Y:C; ab_bid=dfe9b8057f1bdb6b689b31f9de62bc03438f; ab_sr=1.0.1_YTRiNzZhZTBkMmQyYmJiM2Q1YzYzYzVlYTJkNGE0ODIwNzM2N2VjOTFlY2MzYzk3M2FhZGY1YmYwODk5Y2YyZDYyZjFiNWMzOTlhMDUzNDgzMDcxZWRlMjI2MzgyYmI0NDIxMWVmN2ZlMGIxYjlhMTc2OGIxMGJmOTYwZmRjNjQxYjUxOWMyZWEzN2Y4OWMyOGViZTBhNzUxMTgwOTQyYTMwYmE3NzA0MDQzMWUyZWUwYTQwNjE3MmJiMGVkZDNk",

    }
    web = requests.get(urls, headers=header).text
    dom = etree.HTML(web)
    song_id = dom.xpath ('//li//a[contains(@href,"song?id=")]/@href')
    song_name = dom.xpath('//li//a[contains(@href,"song?id=")]/text()')

    a = 0
    for song_id,song_name in zip(song_id,song_name):
        ID = song_id.strip('/song?id=')
        if ("$" in ID) == False:
            url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
            file = open('yiyun.js', 'r').read()
            music = execjs.compile(file)

            params_seckey = music.call("asrsea_params",ID)
            with open('data.json', 'r') as file:
                datas = json.load(file)

            data ={
                "csrf_token": "",
                "params": datas["encText"],
                "encSecKey": datas["encSecKey"]
            }
            music_download = requests.post(url, data=data)

            dict = json.loads(music_download.text)
            mp3_url = dict['data'][0]['url']
            #不知到为什么字典里会有none
            if mp3_url == None:
                continue

            mp3 = requests.get(mp3_url,headers=header).content
            folder_name = "download_music"
            file_name = f'{song_name}.mp3'
            os.makedirs(folder_name, exist_ok=True)
            file_path = os.path.join(folder_name, file_name)
            with open(file_path, 'wb') as file:
                file.write(mp3)


def comment(url ='https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=' ):
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    i = "vlPYFXlp9z8pxQax"
    g = '0CoJUm6Qyw8W8jud'
    e = '010001'
    d = "{\"id\":\"2637060319\",\"lv\":-1,\"tv\":-1,\"csrf_token\":\"356d65aa26bc9fa0d9fea918b9557647\"}"

    encSecKey = "239592847dbf8ea7a5867f3364d7468c5f5507508b21ad8c2e63e04cf648d17eefb2a3aaaedcd14a9a87fe691514fff053104657fff62f7320215c0868924c2023d020f176f1a02f025501a9d39a992f8a5eba5ffb2df5db8da4f4581e4498375ed83443b8fc19c5c3f80db5c931bc1da607db07990a28d52451e2c6496cbe39"
    encText = "tEOn9OYzaurWQV2RnIqq3HG/cROsCe3eJ0aDAjtrlW8YDjYuEZqM34g5VtQFmEinoP07s9f/xWeJ62/atxAdBw2Lh70lc1kZhi2eKb/1HyUZUA6esfcMVBGmm1jxcNeu+MXmiCchletyUhJ4CcLcSmtIsEHq8udCK3PlM0tztZE6zfRWTanVrGPwBBIxVoIIbc0v8HhFWcKjB9y5ugWVpe8d7NdrkJqeSY9bTar9o21dTQruiLiNwE4Xq+hNuvOlub+bqR5d5HKLDmPmK56yVQys845dV4C/3IpY8fBgb6tMKB1AYC8k04BCApShJdqoAuA5JQ/bGvG2piltQ9miLU2IOQmEEcMsw4MfKway47LbzO2Ax3V690gcQ3r2AQzV1Ho4grmvnxFT/JlaRKthHpaMxpSR0+HcPAHNss6abZHZHhNP7cbVZ1LHROxHhozphDzINWG+lHbUnZQtTfDn1fe/DlUkim/qgRsdIagK1oupLdQ9/0HVGobTOXmG5ML34aKcRl6jpq5KBQsSKAOEHSk2XxkTw7KY/0Ch/NRf2MJIWHdBjP+Xy7EaR6FSXHXxcxjemCAAdMGFjkxmnFXfyViOd/l8gJ0I+QDZ4odK+Ic+WTAEm70r3MhLkrc0afWi"
    data = {
        "csrf_token": "",
        "cursor": "-1",
        "offset": "0",
        "orderType": "1",
        "pageNo": "1",  # 评论的页数
        "pageSize": "20",
        "rid": "R_SO_4_2636250351",
        "threadId": "R_SO_4_2636250351",
    }

    def get_encSecKey():
        return '239592847dbf8ea7a5867f3364d7468c5f5507508b21ad8c2e63e04cf648d17eefb2a3aaaedcd14a9a87fe691514fff053104657fff62f7320215c0868924c2023d020f176f1a02f025501a9d39a992f8a5eba5ffb2df5db8da4f4581e4498375ed83443b8fc19c5c3f80db5c931bc1da607db07990a28d52451e2c6496cbe39'

    def get_params(data):
        first = enc_params(data, g)
        second = enc_params(first, i)
        return second

    def to_16(data):  # 补齐16位
        pad = 16 - len(data) % 16
        data += chr(pad) * pad
        return data

    def enc_params(data, key):
        IV = "0102030405060708"
        data = to_16(data)
        aes = AES.new(key=key.encode('UTF-8'), IV=IV.encode('UTF-8'), mode=AES.MODE_CBC)
        bs = aes.encrypt(data.encode('UTF-8'))  # 长度必须是16的倍数

        return str(b64encode(bs), 'UTF-8')

    resp = requests.post(url, data={
        'params': get_params(json.dumps(data)),
        'encSecKey': get_encSecKey()
    })
    all_data = resp.json()

    # 评论区
    for comment in all_data['data']['comments']:
        nickname = comment['user']['nickname']
        content = comment['content']
        print(f"昵称: {nickname}, 评论内容: {content}")

print("====================================================================")
print("==================网易云助手===========================")
print("1.下载网易云单曲")
print("2.下载网易云歌单")
print("3.爬取网易云单曲评论区")
print("4,退出")
download()