from utils import tools
import requests
import threading

def get_aid_list_from_patchy():#TODO
    api_url = ''
    response = requests.get(api_url)
    return response

if __name__ == "__main__":
    url_list = get_aid_list_from_patchy()
    path_cookie = tools.get_url_list_config().path_cookie()
    path_storge_list = tools.get_url_list_config().path_storge_list()
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=tools.cmd_download, args=[url_list, path_cookie, path_storge_list, ]))
    for t in threads:
        t.start()