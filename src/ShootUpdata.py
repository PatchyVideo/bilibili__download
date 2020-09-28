from utils import tools
from bilibili_api import video


#def getHistory_Xml():



#def UploadNew_Xml():

if __name__ == "__main__":
    config = tools.get_json()
    path_storge = config["path_storge"]
    Xml_Dict = tools.getExist_aid_Dict(path_storge)
    for path_storge_single in Xml_Dict:
        url = Xml_Dict[path_storge_single]
        tools.getXml_file(tools.getXml_url(url), path_storge_single)
