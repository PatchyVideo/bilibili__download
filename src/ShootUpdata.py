import requests
import re
import json
import xml.etree.ElementTree as ET
import time
import os

#历史弹幕api:https://api.bilibili.com/x/v2/dm/history?type=1&date=xxxx-xx-xx&oid=xxxxx
def aid_to_url(string):
    if string[:2] == 'av' or string[:2] == 'BV':
        url = "https://www.bilibili.com/video/" + string
    elif string.isdigit():
        url = "https://www.bilibili.com/video/av" + string
    else:
        url = "https://www.bilibili.com/video/BV" + string
    return url

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
    #print(type(response.content.decode()))
    r = response.content.decode()
    xml_name = path + str(time.asctime( time.localtime(time.time()) )) + '.xml'
    with open('data.xml', 'w') as f:
        f.write(r.text)


#def getHistory_Xml(data,oid):

#def UploadNew_Xml():

def getExist_Xml_Dict(path_storge):
    dict = {}
    for avs in os.listdir(path_storge):
        path_storge_single = path_storge + avs + "\\"
        url = aid_to_url(avs)
        dict[path_storge_single] = url
    return dict

def get_json():
    f = open("config.json", encoding='utf-8')
    config = json.load(f)
    return config

if __name__ == "__main__":
    config = get_json()
    path_storge = config["path_storge"]
    Xml_Dict = getExist_Xml_Dict(path_storge)
    for path_storge_single in Xml_Dict:
        url = Xml_Dict[path_storge_single]
        getXml_file(getXml_url(url), path_storge_single)
