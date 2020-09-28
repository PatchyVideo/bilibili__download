from utils import tools

if __name__ == "__main__":
    config = tools.get_json()
    path_storge = config["path_storge"]
    aid_Dict = tools.getExist_aid_Dict(path_storge)
    for path_storge_single in aid_Dict:
        url = aid_Dict[path_storge_single]
        tools.StrToJson(tools.GetCommentFromSingle(url), path_storge_single)