import threading
from utils import tools

if __name__ == "__main__":
    url_list, path_cookie, path_storge = tools.get_url_list_config()
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=tools.cmd_download, args=[url_list, path_cookie, path_storge,]))
    for t in threads:
        t.start()

