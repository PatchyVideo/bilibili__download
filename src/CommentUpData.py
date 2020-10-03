from utils import tool

if __name__ == "__main__":
    path_storge_list = tool.get_url_list_config().path_storge_list()
    aid_Dict = tool.getExist_aid_Dict(path_storge_list)
    for path_storge_single in aid_Dict:
        url = aid_Dict[path_storge_single]
        tool.StrToJson(tool.GetCommentFromSingle(url), path_storge_single)