import os
from utils import tool

if __name__ == "__main__":
    path = os.getcwd()
    config = tool.get_json()
    path_storge_list = tool.get_url_list_config().path_storge_list()
    path_cookie = tool.get_url_list_config().path_cookie()
    url_dict = tool.find_download(path_storge_list)
    for url in url_dict:
        path_storge_single = url_dict[url]
        tool.download_video(url, path_storge_single, path_cookie)

