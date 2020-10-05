import time

str = time.localtime(time.time())
def time_str():
    time_obj = time.localtime(time.time())
    str = time_obj.tm_yday + ','
    str = str + time_obj.tm_mon + '.'
    str = str + time_obj.tm_yday + ','
    str = str + time_obj.tm_hour
