import os
import threading
import json

def make_file(url, path_storge):
    path_storge_single = path_storge + url[31:]
    if os.path.exists(path_storge_single):
        print(path_storge_single + "paths is exist>>>>")
    else:
        os.makedirs(path_storge_single)
    return path_storge_single

def download_video(url, path_storge, path_cookie):
    path_storge_single = make_file(url, path_storge)
    cmd = 'you-get -o  ' + path_storge_single + ' -c ' + path_cookie  + ' --playlist '  + url
    os.system(cmd)
    print(url[31:] + "下载完成")

def get_url_from_file(path_aid):
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

def normal_url(string):
    if string[:2] == 'av' or string[:2] == 'BV':
        url = "https://www.bilibili.com/video/" + string
    elif string.isdigit():
        url = "https://www.bilibili.com/video/av" + string
    else:
        url = "https://www.bilibili.com/video/BV" + string
    return url

def get_json():
    f = open("config.json", encoding='utf-8')
    config = json.load(f)
    return config

def get_url_list_config():
    path = os.getcwd()
    config = get_json()
    path_storge = config["path_storge"]
    path_cookie = path + "\\cookies.sqlite"
    path_aid = path + config["path_aid"]
    url_list = get_url_from_file(path_aid)
    #lists = [url_list, path_cookie, path_storge, ]
    return url_list, path_cookie, path_storge

def cmd_download(url_list, path_cookie, path_storge):
    for url in url_list:
        if url[31:] in os.listdir(path_storge):
            print(url[33:] + '已存在，正在跳过')
        else:
            download_video(url, path_storge, path_cookie)

if __name__ == "__main__":
    url_list, path_cookie, path_storge = get_url_list_config()
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=cmd_download, args=[url_list, path_cookie, path_storge,]))
    for t in threads:
        t.start()

