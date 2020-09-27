from bilibili_api import video
import json

def aid_to_url(string):
    if string[:2] == 'av' or string[:2] == 'BV':
        url = "https://www.bilibili.com/video/" + string
    elif string.isdigit():
        url = "https://www.bilibili.com/video/av" + string
    else:
        url = "https://www.bilibili.com/video/BV" + string
    return url

def GetCommentFromSingle(str):
    comment = video.get_comments(bvid=str)
    comment_list = []
    for lines in comment:
        single = {
            "user_mid": lines['member']['mid'],
            "user_name": lines['member']['uname'],
            "content":  lines['content']['message']
        }
        comment_list.append((single))
    return comment_list

