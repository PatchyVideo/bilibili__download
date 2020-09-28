import os
import json
from bilibili_api import video
import time
import re
import requests

def getExist_aid_Dict(path_storge):#返回已经下载的视频aid
    dict = {}
    for avs in os.listdir(path_storge):
        path_storge_single = path_storge + avs + "\\"
        url = aid_to_url(avs)
        dict[path_storge_single] = url
    return dict

def aid_to_url(string):#将av/BV号转为url
    if string[:2] == 'av' or string[:2] == 'BV':
        url = "https://www.bilibili.com/video/" + string
    elif string.isdigit():
        url = "https://www.bilibili.com/video/av" + string
    else:
        url = "https://www.bilibili.com/video/BV" + string
    return url

def download_video(url, path_storge, path_cookie):#下载单个视频,提供url,存储单个文件夹,cookies的位置
    path_storge_single = make_file(url, path_storge)
    cmd = 'you-get -o  ' + path_storge_single + ' -c ' + path_cookie  + ' --playlist '  + url
    os.system(cmd)
    print(url[31:] + "下载完成")

def make_file(url, path_storge):#创建视频文件夹
    path_storge_single = path_storge + url[31:]
    if os.path.exists(path_storge_single):
        print(path_storge_single + "paths is exist>>>>")
    else:
        os.makedirs(path_storge_single)
    return path_storge_single

def get_json():#从config取得设置
    f = open("config.json", encoding='utf-8')
    config = json.load(f)
    return config

def cmd_download(url_list, path_cookie, path_storge):#用一个列表的aid下载多个视频
    for url in url_list:
        if url[31:] in os.listdir(path_storge):
            print(url[33:] + '已存在，正在跳过')
        else:
            download_video(url, path_storge, path_cookie)

class _bv2av() :#avbv相互转化
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608
    def __init__(self) :
        for i in range(58):
            self.tr[self.table[i]]=i

    def dec(self, x) :
        r = 0
        for i in range(6):
            r += self.tr[x[self.s[i]]] * 58 ** i
        return (r - self.add) ^ self.xor

    def enc(self, x) :
        x = (x ^ self.xor) + self.add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[self.s[i]] = self.table[x // 58 ** i % 58]
        return ''.join(r)

def find_download(path_storge):#查找为下载完的视频文件
    dict = {}
    for avs in os.listdir(path_storge):
        path_storge_single = path_storge + avs + "\\"
        for file in os.listdir(path_storge_single):
            if "download" in file:
                url = aid_to_url(avs)
                dict[url] = path_storge_single
    return dict

def GetCommentFromSingle(str):#从单个视频获取评论,返回一个列表
    BV = str[31:]
    if BV[:2] == 'av':
        BV = _bv2av.enc(BV)
    comment = video.get_comments(bvid=BV)
    comment_list = []
    for lines in comment:
        single = {
            "user_mid": lines['member']['mid'],
            "user_name": lines['member']['uname'],
            "content":  lines['content']['message']
        }
        comment_list.append((single))
    return comment_list

def StrToJson(comment_list, path):#将json列表存到文件中
    comment_json = json.dump(comment_list)
    json_name = path + + str(time.asctime( time.localtime(time.time()) ))
    with open(json_name, 'w') as f:
        f.write(comment_json)

def getXml_url(url):#通过视频的url得到弹幕的url
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36"}
    response= requests.get(url,headers)
    html = response.content.decode()
    cid = re.findall(r'("cid":)([0-9]+)', html)
    cid = cid[0][-1]
    xml_url = "https://comment.bilibili.com/{}.xml".format(cid)
    return xml_url

def getXml_file(xml_url, path):#通过弹幕的URL得到弹幕的url文件
    response = requests.get(xml_url)
    r = response.content.decode()
    xml_name = path + str(time.asctime( time.localtime(time.time()) )) + '.xml'
    with open(xml_name, 'w') as f:
        f.write(r.text)

def get_url_from_file(path_aid):#从txt文档读取aid列表
    datas = []
    if os.path.exists(path_aid):
        with open(path_aid, "r") as f:
            data = f.readlines()
            for line in data:
                line = line.rstrip("\n")
                datas.append(aid_to_url(line))
            return datas
    else:
        print("url list do not exist>>>>")

def get_url_list_config():#从config文件得到url列表,cookie的位置和存储位置
    path = os.getcwd()
    config = get_json()
    path_storge = config["path_storge"]
    path_cookie = path + "\\cookies.sqlite"
    path_aid = path + config["path_aid"]
    url_list = get_url_from_file(path_aid)
    return url_list, path_cookie, path_storge