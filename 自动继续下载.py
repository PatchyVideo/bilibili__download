import os
import json
def download_video(url, path_storge_single, path_cookie):
    cmd = 'you-get -o ' + path_storge_single + ' -c ' + path_cookie  + ' --playlist '  + url
    os.system(cmd)
    print(url[31:] + "下载完成")

def find_download(path_storge):
    dict = {}
    for avs in os.listdir(path_storge):
        path_storge_single = path_storge + avs + "\\"
        for file in os.listdir(path_storge_single):
            if "download" in file:
                url = get_url(avs)
                dict[url] = path_storge_single
    return dict

def get_json():
    f = open("config.json", encoding='utf-8')
    config = json.load(f)
    return config

def get_url(avid):
    url = "https://www.bilibili.com/video/" + avid
    return url

if __name__ == "__main__":
    path = os.getcwd()
    config = get_json()
    path_storge = config["path_storge"]
    path_cookie = path + "\\cookies.sqlite"
    url_dict = find_download(path_storge)
    for url in url_dict:
        path_storge_single = url_dict[url]
        download_video(url, path_storge_single, path_cookie)

