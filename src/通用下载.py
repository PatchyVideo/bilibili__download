import threading
from utils import tool

if __name__ == "__main__":
    url_list = tool.get_url_list_config().url_list()
    path_cookie = tool.get_url_list_config().path_cookie()
    path_storge_list = tool.get_url_list_config().path_storge_list()
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=tool.cmd_download, args=[url_list, path_cookie, path_storge_list,]))
    for t in threads:
        t.start()

