import os
import json

def getExist_aid_Dict(path_storge):
    dict = {}
    for avs in os.listdir(path_storge):
        path_storge_single = path_storge + avs + "\\"
        url = aid_to_url(avs)
        dict[path_storge_single] = url
    return dict


def aid_to_url(string):#将av号转为url
    if string[:2] == 'av' or string[:2] == 'BV':
        url = "https://www.bilibili.com/video/" + string
    elif string.isdigit():
        url = "https://www.bilibili.com/video/av" + string
    else:
        url = "https://www.bilibili.com/video/BV" + string
    return url

def download_video(url, path_storge, path_cookie):
    path_storge_single = make_file(url, path_storge)
    cmd = 'you-get -o  ' + path_storge_single + ' -c ' + path_cookie  + ' --playlist '  + url
    os.system(cmd)
    print(url[31:] + "下载完成")

def make_file(url, path_storge):
    path_storge_single = path_storge + url[31:]
    if os.path.exists(path_storge_single):
        print(path_storge_single + "paths is exist>>>>")
    else:
        os.makedirs(path_storge_single)
    return path_storge_single

def get_json():
    f = open("config.json", encoding='utf-8')
    config = json.load(f)
    return config

def cmd_download(url_list, path_cookie, path_storge):
    for url in url_list:
        if url[31:] in os.listdir(path_storge):
            print(url[33:] + '已存在，正在跳过')
        else:
            download_video(url, path_storge, path_cookie)

class _bv2av() :
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

def download_video(url, path_storge_single, path_cookie):
    cmd = 'you-get -o ' + path_storge_single + ' -c ' + path_cookie  + ' --playlist '  + url
    os.system(cmd)
    print(url[31:] + "下载完成")
