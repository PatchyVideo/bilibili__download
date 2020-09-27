import os
import threading
import json
from utils import tools

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
                datas.append(tools.aid_to_url(line))
            return datas
    else:
        print("url list do not exist>>>>")

def get_url_list_config():
    path = os.getcwd()
    config = tools.get_json()
    path_storge = config["path_storge"]
    path_cookie = path + "\\cookies.sqlite"
    path_aid = path + config["path_aid"]
    url_list = get_url_from_file(path_aid)
    return url_list, path_cookie, path_storge

if __name__ == "__main__":
    url_list, path_cookie, path_storge = get_url_list_config()
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=tools.cmd_download, args=[url_list, path_cookie, path_storge,]))
    for t in threads:
        t.start()

