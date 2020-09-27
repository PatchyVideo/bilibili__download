import os
import json
from utils import tools

def find_download(path_storge):
    dict = {}
    for avs in os.listdir(path_storge):
        path_storge_single = path_storge + avs + "\\"
        for file in os.listdir(path_storge_single):
            if "download" in file:
                url = tools.aid_to_url(avs)
                dict[url] = path_storge_single
    return dict

if __name__ == "__main__":
    path = os.getcwd()
    config = tools.get_json()
    path_storge = config["path_storge"]
    path_cookie = path + "\\cookies.sqlite"
    url_dict = find_download(path_storge)
    for url in url_dict:
        path_storge_single = url_dict[url]
        tools.download_video(url, path_storge_single, path_cookie)

