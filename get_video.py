import psycopg2
import requests
import time
import os

import multiprocessing as mp
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

from config import Config
from common import Bv2av, DbBase

class Download():

    def __init__(self):
        pass


    def make_file(self, url, path_storge):
        """make a file named by av"""
        path_storge_single = path_storge + url[31:]
        if os.path.exists(path_storge_single):
            pass
        else:
            os.mkdir(path_storge_single, mode=0o4755)
        return path_storge_single


    def download(self, param):
        """
        download single video 
        parame = (url, file path, cookies path
        """
        url, path_storge = param
        av_url = url.split("?")[0]
        path = "/smb/J/" + url.split("?")[0].split("/")[-1] + "/"
        bv_trans = Bv2av()
        av = "av" + url.split("?")[0].split("av")[-1]
        bv = bv_trans.enc(int(av[2:]))
        if not self.if_video_exist(path):
            path_storge_single = self.make_file(url, path_storge)
            cmd = 'you-get -o ' + path_storge_single + ' -c ' + \
                "cookies.sqlite" + ' --playlist ' + av_url
            if os.system(cmd) == 0:
                log = "[" + str(time.asctime(time.localtime(time.time()))
                                ) + "]" + url + "downloaded"
                with open("log.txt", "a") as f:
                    f.write("\n" + log)
            else:
                log = "[" + str(time.asctime(time.localtime(time.time()))
                                ) + "]" + url + "fail"
                with open("log.txt", "a") as f:
                    f.write("\n" + log)
        else:
            pass


    def if_video_exist(self, path):
        "check video has been downloaded"
        try:
            if os.listdir(path):
                for file in os.listdir(path):
                    if ".download" in file:
                        return False
                    elif ".mp4" or "flv" in file:
                        return True
                    else:
                        return False
                else:
                    return False
        except:
            return False


    def go(self):
        url_test = Db()
        time_, url_list = url_test.get_url()
        if url_list:
            for url in url_list:
                path = "/smb/J/" + url.split("?")[0].split("/")[-1] + "/"
                if self.if_video_exist(path):
                    url_test.delete(url)
            pool = mp.Pool(5)  # five thread
            pool.map(self.download, [
                     (url.split("?")[0], Config.path_storge_root) for url in url_list])
            pool.close()
            pool.join()
            url_test.close()


class Db(DbBase):

    def get_all_url(self):
        sql = "select * from url_q"
        self.cursor.execute(sql)
        rows=self.cursor.fetchall()
        if rows:
            time = rows[0][0]
            url_list = [row[1] for row in rows]
            return url_list
        else:
            return rows
    
    
    def updata(self, url_list):
        sql = "insert into url_q (time, url) select %s, %s where not exists (select * from url_q where url = (%s)) "
        if url_list:
            for url in url_list:
                if "av" in url:
                    time_now = int(time.time())
                    parameter = (time_now, url, url)
                    self.cursor.execute(sql, parameter)
        self.connection.commit()
        
    
    def delete(self, url):
        sql = "delete from url_q where url=%s;"
        parameter = (url,)
        self.cursor.execute(sql, parameter)
        self.connection.commit()



def check_bv(url):
    if "av" in url:
        _bv = Bv2av()
        bv = _bv.enc(int(url.split("?")[0].split("av")[-1]))
        url = "http://api.bilibili.com/x/web-interface/view?bvid={}".format(bv)
        
    resp = requests.get(url).json()
    if resp["message"] == "稿件不可见":
        return True


def checking_failure():
    url_db = Db()
    url_list = url_db.get_all_url()
    for url in url_list:
        if check_bv(url):
            url_db.delete(url)
            log = "[" + str(time.asctime(time.localtime(time.time())))+ "]" + url + "失效"
            with open("log.txt", "a") as f:
                f.write("\n" + log)
    url_db.close()


def bili_last_24hrs():
    now = (datetime.utcnow() - timedelta(hours = 24)).isoformat()
    ret = requests.post("https://thvideo.tv/be/queryvideo.do", json={'query': f'site:bilibili NOT 游戏 date:>="{now}"', 'order': 'video_latest', 'lang': 'CHS', 'offset': 0, 'limit': 10000}).json()
    return [item['item']['url'] for item in ret['data']['videos']]


def updata_url():
    url_q_db = Db()
    url_list = bili_last_24hrs()
    url_q_db.updata(url_list)
    url_q_db.close()
    log = "Updata: " + str(len(url_list)) + " " + str(time.asctime(time.localtime(time.time())))
    with open("get_video.txt", "a") as f:
        f.write("\n" + log)    

    
def download():
    downloader = Download()
    downloader.go_db()


def main():
    scheduler = BlockingScheduler()
    updata_url()
    download()
    checking_failure()
    scheduler.add_job(updata_url, 'interval', seconds=7200)
    scheduler.add_job(download, 'interval', seconds=14400)
    scheduler.add_job(checking_failure, 'cron', day_of_week='0-6', hour=12, minute=0)
    scheduler.start()


if __name__ == "__main__":
    main()