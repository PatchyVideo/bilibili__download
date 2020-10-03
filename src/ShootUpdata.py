from utils import tool

if __name__ == "__main__":
    path_storge_list = tool.get_url_list_config().path_storge_list()
    Xml_Dict = tool.getExist_aid_Dict(path_storge_list)
    for path_storge_single in Xml_Dict:
        url = Xml_Dict[path_storge_single]
        tool.getXml_file(tool.get_damu(url), path_storge_single)
