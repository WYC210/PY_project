import time

import requests
import bs4
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
import json
url = f"https://dytt89.com/"
header = {

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}



text = requests.get(url, headers=header)
text.encoding = 'gb2312'



obj = re.compile(r'2024必看热片.*?<ul>(?P<ul>.*?)</ul>',re.S)
obj1 = re.compile(r"<li>.*?/(?P<href>.*?)'",re.S)
obj2 = re.compile(r"《(?P<name>.*?)》",re.S)
text = obj.finditer(text.text)
dic = {}
for i in text:
    ul =i.group('ul')


    movie_names = obj2.finditer(ul)
    result = obj1.finditer(ul)
    for k, j in zip(movie_names, result):
        key = k.group('name')
        href = url + j.group('href')
        dic[key] = href

print(dic)


# 北京新发地菜价
def vegetable():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }
    url = "http://www.xinfadi.com.cn/getPriceData.html"
    print("执行代码会有些慢，防止被服务器拉黑")
    num1 = eval(input("输入你想爬的起始页数"))
    num2 = eval(input("输入你想爬的终止页数"))
    for i in range(num1,num2+1):
        time.sleep(1)
        date = {
            "count"
            :
                "464572",
            "current"
            :
                f"{i}",
            "limit"
            :
                "20"
        }
        response = requests.post(url, headers=header,data=date)
        text = response.json()
        with open('vegetable.txt', 'a', encoding='utf-8') as f:
            for i in text['list']:
                f.write(
                    f"蔬菜名字: {i['prodName']}  最低价: {i['lowPrice']} 最高价: {i['highPrice']} 平均价格: {i['avgPrice']} 规格: {i['specInfo']} 产地: {i['place']} 单位: {i['unitInfo']} 时间: {i['pubDate']} \n")
                # print(i['prodName'])
                # print(i['lowPrice'])
                # print(i['highPrice'])
                # print(i['avgPrice'])
                # print(i['place'])
                # print(i['unitInfo'])
                # print(i['pubDate'])
    print("完成写入")

# 中国天气网获取天气
def weather():
    url = "https://i.tq121.com.cn/j/webgis_v2/city.json"
    header = {
        "referer": "https://www.weather.com.cn/",
        "Cookie": "ab_jid=4dc76423b3b0e37a4226ab044b8bd8cfd9a7; ab_jid_BFESS=4dc76423b3b0e37a4226ab044b8bd8cfd9a7; BDUSS_BFESS=m13VERLaHBZQkJkeEttMnd4dmhyRFlmOEYxc0c1TUIwYlhFTFBSUDVMTkh1SmxtRUFBQUFBJCQAAAAAAQAAAAEAAABqXfQNtLvI~cvqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEcrcmZHK3Jmd; H_WISE_SIDS_BFESS=60841_60854_60887_60875; BAIDUID_BFESS=9BC5B1FC93BA6F88BD3BB77A2BC74A78:FG=1; ZFY=bt6bReJ0xr7piGR2tYhBd2luJ:BJnqE9L6Ny7:AWBa:B0Y:C; ab_bid=dfe9b8057f1bdb6b689b31f9de62bc03438f; ab_sr=1.0.1_YTRiNzZhZTBkMmQyYmJiM2Q1YzYzYzVlYTJkNGE0ODIwNzM2N2VjOTFlY2MzYzk3M2FhZGY1YmYwODk5Y2YyZDYyZjFiNWMzOTlhMDUzNDgzMDcxZWRlMjI2MzgyYmI0NDIxMWVmN2ZlMGIxYjlhMTc2OGIxMGJmOTYwZmRjNjQxYjUxOWMyZWEzN2Y4OWMyOGViZTBhNzUxMTgwOTQyYTMwYmE3NzA0MDQzMWUyZWUwYTQwNjE3MmJiMGVkZDNk",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    data = response.text
    data = data.replace('weacity(', '')
    data = data.rstrip(')')
    data = json.loads(data)
    with open('weather.txt', 'w', encoding='utf-8') as f:
        for i in data:
            urls = "https://www.weather.com.cn/weather1d/"
            new_url = urls + i + '.shtml'

            weather = requests.get(new_url, headers=header)
            weather.encoding = 'utf-8'
            soup = bs4.BeautifulSoup(weather.text, 'html.parser')
            inputs = soup.find_all('input')
            hidden_title_input = soup.find('input', id='hidden_title')
            value = hidden_title_input['value']
            f.write(f"{data[i]['n']} : {value}\n")



# 爬取电影
def movie():
    url = 'https://1daifu.com/mahua/1.html'
    header = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    movies = soup.find('ul', class_='screen_list sx_tz clearfix')
    print(movies)

#  梨视频下载
def li_movie():
    url = 'https://www.pearvideo.com/video_1796529'
    coutId = url.split('_')[1]

    video_url = f'https://www.pearvideo.com/videoStatus.jsp?contId={coutId}&mrd=0.7135740481567494'

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        "referer": f"{url}"
    }
    text = requests.get(video_url, headers=header)
    result = text.json()
    video_url = result['videoInfo']['videos']['srcUrl']
    systemTime = result['systemTime']
    video_url = video_url.replace(f'{systemTime}', f'cont-{coutId}')
    with open('video.mp4', 'wb') as f:
        f.write(requests.get(video_url, headers=header).content)

# 下载网易云歌曲
def yiyun(url ="https://music.163.com/weapi/comment/resource/comments/get?csrf_token="):
    # "/weapi/privacy/info/get/v2?csrf_token="
    # "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
    url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    i = "vlPYFXlp9z8pxQax"
    g = '0CoJUm6Qyw8W8jud'
    e = '010001'
    d = "{\"id\":\"2601642946\",\"lv\":-1,\"tv\":-1,\"csrf_token\":\"356d65aa26bc9fa0d9fea918b9557647\"}"

    encSecKey="239592847dbf8ea7a5867f3364d7468c5f5507508b21ad8c2e63e04cf648d17eefb2a3aaaedcd14a9a87fe691514fff053104657fff62f7320215c0868924c2023d020f176f1a02f025501a9d39a992f8a5eba5ffb2df5db8da4f4581e4498375ed83443b8fc19c5c3f80db5c931bc1da607db07990a28d52451e2c6496cbe39"
    encText ="tEOn9OYzaurWQV2RnIqq3HG/cROsCe3eJ0aDAjtrlW8YDjYuEZqM34g5VtQFmEinoP07s9f/xWeJ62/atxAdBw2Lh70lc1kZhi2eKb/1HyUZUA6esfcMVBGmm1jxcNeu+MXmiCchletyUhJ4CcLcSmtIsEHq8udCK3PlM0tztZE6zfRWTanVrGPwBBIxVoIIbc0v8HhFWcKjB9y5ugWVpe8d7NdrkJqeSY9bTar9o21dTQruiLiNwE4Xq+hNuvOlub+bqR5d5HKLDmPmK56yVQys845dV4C/3IpY8fBgb6tMKB1AYC8k04BCApShJdqoAuA5JQ/bGvG2piltQ9miLU2IOQmEEcMsw4MfKway47LbzO2Ax3V690gcQ3r2AQzV1Ho4grmvnxFT/JlaRKthHpaMxpSR0+HcPAHNss6abZHZHhNP7cbVZ1LHROxHhozphDzINWG+lHbUnZQtTfDn1fe/DlUkim/qgRsdIagK1oupLdQ9/0HVGobTOXmG5ML34aKcRl6jpq5KBQsSKAOEHSk2XxkTw7KY/0Ch/NRf2MJIWHdBjP+Xy7EaR6FSXHXxcxjemCAAdMGFjkxmnFXfyViOd/l8gJ0I+QDZ4odK+Ic+WTAEm70r3MhLkrc0afWi"
    data={
        "csrf_token": "",
        "cursor": "-1",
        "offset": "0",
        "orderType": "1",
        "pageNo": "1", #评论的页数
        "pageSize": "20",
        "rid": "R_SO_4_2636250351",
        "threadId": "R_SO_4_2636250351",
    }

    def get_encSecKey():
        return '239592847dbf8ea7a5867f3364d7468c5f5507508b21ad8c2e63e04cf648d17eefb2a3aaaedcd14a9a87fe691514fff053104657fff62f7320215c0868924c2023d020f176f1a02f025501a9d39a992f8a5eba5ffb2df5db8da4f4581e4498375ed83443b8fc19c5c3f80db5c931bc1da607db07990a28d52451e2c6496cbe39'
    def get_params(data):
        first = enc_params(data,g)
        second = enc_params(first,i)
        return second
    def to_16(data): # 补齐16位
        pad = 16 - len(data) % 16
        data += chr(pad) * pad
        return data
    def enc_params(data,key):
        IV="0102030405060708"
        data = to_16(data)
        aes = AES.new(key=key.encode('UTF-8'),IV=IV.encode('UTF-8'),mode=AES.MODE_CBC)
        bs = aes.encrypt(data.encode('UTF-8'))# 长度必须是16的倍数

        return str(b64encode(bs),'UTF-8')


    resp = requests.post(url,data={
        'params': get_params(json.dumps(data)),
        'encSecKey': get_encSecKey()
        })
    all_data = resp.json()

    #评论区
    for comment in all_data['data']['comments']:
        nickname = comment['user']['nickname']
        content = comment['content']
        print(f"昵称: {nickname}, 评论内容: {content}")
    print(all_data)
    """function a(a) {  #这个是一个随机生成16位字符串
            var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
            for (d = 0; a > d; d += 1)
                e = Math.random() * b.length,
                e = Math.floor(e),
                c += b.charAt(e);
            return c
        }
        function b(a, b) { 把数据用cbc格式加密了！！！！
            var c = CryptoJS.enc.Utf8.parse(b) 密钥
              , d = CryptoJS.enc.Utf8.parse("0102030405060708")  加密模式
              , e = CryptoJS.enc.Utf8.parse(a) 把随机数加密了
              , f = CryptoJS.AES.encrypt(e, c, {  二次加密
                iv: d,
                mode: CryptoJS.mode.CBC # 模式
            });
            return f.toString() 转编码
        }
        function c(a, b, c) { 也是加密
            var d, e;
            return setMaxDigits(131),
            d = new RSAKeyPair(b,"",c),
            e = encryptedString(d, a)
        }
        function d(d, e, f, g) { d:数据 e: '010001' f: ### g: '0CoJUm6Qyw8W8jud'
            var h = {}
              , i = a(16); 电调用a函数
            return h.encText = b(d, g),  一次加密
            h.encText = b(h.encText, i), 二次加密
            h.encSecKey = c(i, e, f), 内容加密
            h
        }"""

# 爬取小说
import requests

url = 'https://bookapi.zongheng.com/api/chapter/getChapterList'
header = {
"x-trace-id":
"400c9c4bec7a82f8",

"host":
"bookapi.zongheng.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": 'https://read.zongheng.com/',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}
data = {
   " bookId": "1322528"
}

# 使用 json 参数
response = requests.post(url, headers=header,data=data)
response.encoding = 'utf-8'

try:
    print(response.json())
except ValueError:
    print("响应不是有效的 JSON:", response.text)
