from bilibili_api import video
import json
import time
from utils import tools


def GetCommentFromSingle(str):
    BV = str[31:]
    if BV[:2] == 'av':
        BV = tools._bv2av.enc(BV)
    comment = video.get_comments(bvid=BV)
    comment_list = []
    for lines in comment:
        single = {
            "user_mid": lines['member']['mid'],
            "user_name": lines['member']['uname'],
            "content":  lines['content']['message']
        }
        comment_list.append((single))
    return comment_list

def StrToJson(comment_list, path):
    comment_json = json.dump(comment_list)
    json_name = path + + str(time.asctime( time.localtime(time.time()) ))
    with open(json_name, 'w') as f:
        f.write(comment_json)

if __name__ == "__main__":
    config = tools.get_json()
    path_storge = config["path_storge"]
    aid_Dict = tools.getExist_aid_Dict(path_storge)
    for path_storge_single in aid_Dict:
        url = aid_Dict[path_storge_single]
        StrToJson(GetCommentFromSingle(url), path_storge_single)