from utils import video
import ctypes
import os
import platform
import requests
import json
import re
import time


def get_free_space_mb(folder):
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024/1024.

def getExist_aid_Dict(path_storge_list):#返回已经下载的视频aid
    dict = {}
    for path_storge in path_storge_list:
        for avs in os.listdir(path_storge):
            if '$RECYCLE.BIN' in avs:
                continue
            else:
                path_storge_single = path_storge + avs + "\\"
                url = aid_to_url(avs)
                dict[path_storge_single] = url
    return dict

def getExist_aid_list(path_storge_list):
    aid_list = []
    for path_storge in path_storge_list:
        for aid in os.listdir(path_storge):
            if '$RECYCLE.BIN' in aid:
                continue
            elif if_video_exist(path_storge + aid):
                aid_list.append(aid)
        return aid_list

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
    path = os.getcwd() + "/config.json"
    f = open(path, encoding='utf-8')
    config = json.load(f)
    return config

def cmd_download(url_list, path_cookie, path_storge_list):#用一个列表的aid下载多个视频
    count = 0
    path_storge = path_storge_list[count]
    for url in url_list:
        if get_free_space_mb(path_storge) < 1:
            count = count + 1
            path_storge = path_storge_list[count]
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

def find_download(path_storge_list):#查找为下载完的视频文件
    dict = {}
    for path_storge in path_storge_list:
        for avs in os.listdir(path_storge):
            if '$RECYCLE.BIN' in avs:
                continue
            else:
                path_storge_single = path_storge + avs + "\\"
                for file in os.listdir(path_storge_single):
                    if "download" in file:
                        url = aid_to_url(avs)
                        dict[url] = path_storge_single
    return dict

def GetCommentFromSingle(str):#从单个视频获取评论,返回一个列表
    str = str[31:]
    if str[:2] == 'av':
        BV = _bv2av().enc(int(str[2:]))
    try:
        comment = video.get_comments(bvid=BV)
    except:
        return 'err'
    comment_list = []
    for lines in comment:
        single = {
            "user_mid": lines['member']['mid'],
            "user_name": lines['member']['uname'],
            "content":  lines['content']['message']
        },
        comment_list.append(single)
    return json.dumps(comment_list)

def StrToJson(comment_list, path):#将json列表存到文件中
    for path_file in os.listdir(path):
        if "Comment" in path_file:
            os.remove(path + path_file)
    if comment_list == 'err':
        with open(path + "Commentdispear.json", 'w') as f:
            f.write("视频已神隐")
            print("ShiXiao")
    else:
        comment_json = json.dumps(comment_list)
        json_name = path + str(time.asctime( time.localtime(time.time()) )) + 'Comment.json'
        with open(json_name, 'w') as f:
            f.write(comment_json)

def getXml_url(url):#通过视频的url得到弹幕的url
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36"}
    response= requests.get(url,headers)
    #print(response)
    if str(response) == '<Response [200]>':
        xml_url = 'err'
    else:
        html = response.content.decode()
        cid = re.findall(r'("cid":)([0-9]+)', html)
        cid = cid[0][-1]
        xml_url = "https://comment.bilibili.com/{}.xml".format(cid)
    return xml_url

def getXml_file(xml_file, path):#通过弹幕的URL得到弹幕的url文件
    if xml_file == 'err':
        print("lost")
    else:
        xml_name = path + str(time.asctime( time.localtime(time.time()))) + '.xml'
        for path_file in os.listdir(path):
            if ".xml" in path_file:
                print(path + path_file)
                os.remove(path + path_file)
        with open(xml_name, 'w') as f:
            f.write(xml_file)

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

def normall_avbv(x):
    if x[:2] == 'BV':
       x = _bv2av().dec(x)
       x = 'av' + str(x)
    elif x[:2] == 'av':
        pass
    else:
        return 'err'
    return x

def get_file_path_from_aid(aid):
    path_storge_list = get_url_list_config().path_storge_list()
    for path_storge in path_storge_list:
        for file in os.listdir(path_storge):
            if '$RECYCLE.BIN' in file:
                continue
            elif aid in file:
                path = path_storge + file + '\\'
                return path
                break
    return 'err'

class get_url_list_config():#从config文件得到url列表,cookie的位置和存储位置

    def __init__(self):
        self.path = os.getcwd()
        self.config = get_json()

    def path_cookie(self):
        path_cookie = self.path + "/cookies.sqlite"
        return path_cookie

    def url_list(self):
        path_aid = self.path + "/aid.txt"
        url_list = get_url_from_file(path_aid)
        return url_list

    def path_storge_list(self):
        path_storge_list = self.config["path_storge_list"]
        return path_storge_list

def get_damu(url):
    aid = url[33:]
    try:
        rep = video.get_danmaku(aid = aid).content.decode("utf-8")
    except:
        rep = 'err'
    return rep

def if_video_exist(path):
    for file in os.listdir(path):
        if ".mp4" or "flv" in file:
            return 1
        else:
            return 0

def dirsize(dirpath):
    filenames_list = os.listdir(dirpath)
    total_size = 0
    for filename in filenames_list:
        filepath = os.path.join(dirpath, filename)
        if os.path.isfile(filepath):
            filesize = os.path.getsize(filepath)
            total_size += filesize
        else:
            total_size += dirsize(filepath)
    return total_size

class web_tools():

    def __init__(self):
        self.path_storge_list = get_url_list_config().path_storge_list()
        self.Exist_aid_list = getExist_aid_list(self.path_storge_list)

    def get_video_count(self):
        count = len(self.Exist_aid_list)
        return {'video_count': count}

    def Is_video_exist(self, string):
        if string in self.Exist_aid_list:
            return {'Is_video_exist':'Exist'}
        else:
            return {'Is_video_exist':'UnExist'}

    def uplaod_backup(self, string):
        string = normall_avbv(string)
        url = aid_to_url(string)
        path_storge_list = get_url_list_config().path_storge_list()
        path_cookie = get_url_list_config().path_cookie()
        count = 0
        path_storge = path_storge_list[count]
        if get_free_space_mb(path_storge) < 1:
            count = count + 1
            path_storge = path_storge_list[count]
        if url[31:] in os.listdir(path_storge):
            print(url[33:] + '已存在，正在跳过')
        download_video(url, path_storge, path_cookie)
        return {"state": 'sus'}

    def get_comment(self, string):
        path = get_file_path_from_aid(string)
        if path == 'err':
            return {'state' : 'fail'}
        else:
            for comment_json_file in os.listdir(path):
                if "Comment" in comment_json_file:
                    with open(path + comment_json_file, 'r') as f:
                        comment_dict = json.load(f)
                return comment_dict

    def dir_size(self):
        size = 0
        for path_storge in self.path_storge_list:
            size = size + dirsize(path_storge)
        return size/1000/1000/1000


'''
def updata_baidu_disk():
    return
'''