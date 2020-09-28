import os
from utils import tools

if __name__ == "__main__":
    path = os.getcwd()
    config = tools.get_json()
    path_storge = config["path_storge"]
    path_cookie = path + "\\cookies.sqlite"
    url_dict = tools.find_download(path_storge)
    for url in url_dict:
        path_storge_single = url_dict[url]
        tools.download_video(url, path_storge_single, path_cookie)

