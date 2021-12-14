import psycopg2
import time
import os
import cv2
import json
import sys

from config import Config
from common import Bv2av, DbBase

class Video(object):

    def __init__(self, av=None, name=None, path=None):
        self.av = av
        self.url = "https://www.bilibili.com/video/" + Bv2av().enc(int(av[2:]))
        self.bv = Bv2av().enc(int(av[2:]))
        self.aid = int(av[2:])
        self.name = name
        self.path = path
        self.size = float(os.path.getsize(path)/1024/1024)
        self.get_video_duration_and_frames(path)

    
    def get_video_duration_and_frames(self, filename):

        cap = cv2.VideoCapture(filename)
        if cap.isOpened():
            self.rate = cap.get(5)
            frame_num = cap.get(7)
            if frame_num < 2**31 and frame_num > 0:
                self.frame_num = frame_num
            else:
                self.frame_num = 0
            self.duration = self.frame_num/self.rate
        else:
            self.rate = 0
            self.frame_num = 0
            self.duration = 0


class Db(DbBase):
    
    def updata(self, video: Video):
        sql = "insert into video (bv, av, url, name, path, size, length, frame, fps, aid) select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\
            where not exists (select * from video where name = (%s)) "
        parameter = (video.bv, video.av, video.url, video.name, video.path, video.size, video.duration, video.frame_num, video.rate, video.aid, video.name)
        self.cursor.execute(sql, parameter)
        self.connection.commit()
    

    def delete(self, video: Video):
        sql = "delete from video where av=%s;"
        parameter = (video.av,)
        self.cursor.execute(sql, parameter)
        self.connection.commit()



class Storge(object):
    
    def __init__(self):
        self.disk_list = Config.disk_list

        
    def if_video_exist(self, path):
        if path.split("/")[-1] == '$RECYCLE.BIN':
            return False
        try:
            if os.listdir(path):
                for file in os.listdir(path):
                    if ".mp4" or "flv" in file:
                        return True
                    else:
                        return False
            else:
                # os.rmdir(path)
                return False
        except Exception as e:
            print(e)
            return False


    def get_video_name(self, path):
        for file in os.listdir(path):
            if ".mp4" or "flv" in file.split(".")[-1]:
                return file


    def scan(self):
        video_db = Db()
        for disk_path in self.disk_list: 
            for folder in os.listdir(disk_path)[::-1]: 
                if self.if_video_exist(disk_path + folder): 
                    av = folder.split("/")[-1] 
                    path = disk_path + folder + "/"
                    for file in os.listdir(path):
                        if "mp4" == file.split(".")[-1] or "flv" == file.split(".")[-1]:
                            name = file
                            video_path = path + name
                            video = Video(av=av, name=name, path=video_path)
                            try:
                                video_db.updata(video)
                            except:
                                pass
        video_db.close()


if __name__ == "__main__":
    Storge().scan()
    