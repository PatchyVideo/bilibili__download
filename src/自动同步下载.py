from utils import tools
import requests
import threading

def get_aid_list_from_patchy():#TODO
    api_url = ''
    response = requests.get(api_url)
    return response

if __name__ == "__main__":
    url_list = get_aid_list_from_patchy()
    fw, path_cookie, path_storge = tools.get_url_list_config()
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=tools.cmd_download, args=[url_list, path_cookie, path_storge, ]))
    for t in threads:
        t.start()