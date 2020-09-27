import requests
import re
import json
import time
import os
from utils import tools


def getXml_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36"}
    response= requests.get(url,headers)
    html = response.content.decode()
    cid = re.findall(r'("cid":)([0-9]+)', html)
    cid = cid[0][-1]
    xml_url = "https://comment.bilibili.com/{}.xml".format(cid)
    return xml_url

def getXml_file(xml_url, path):
    response = requests.get(xml_url)
    r = response.content.decode()
    xml_name = path + str(time.asctime( time.localtime(time.time()) )) + '.xml'
    with open(xml_name, 'w') as f:
        f.write(r.text)

#def getHistory_Xml(data,oid):

#def UploadNew_Xml():

if __name__ == "__main__":
    config = tools.get_json()
    path_storge = config["path_storge"]
    Xml_Dict = tools.getExist_aid_Dict(path_storge)
    for path_storge_single in Xml_Dict:
        url = Xml_Dict[path_storge_single]
        getXml_file(getXml_url(url), path_storge_single)
