from flask import Flask
from utils.tool import web_tools

app = Flask(__name__)

@app.route("/Count",methods=['GET','POST'])
def Count():
    return web_tools().get_video_count()

@app.route("/Is_exist/<aid>",methods=['GET','POST'])
def Is_exist(aid):
    return web_tools().Is_video_exist(aid)

@app.route("/upload_back/<string>",methods=['GET','POST'])
def upload_backup(string):#avbv all ok
    return web_tools().uplaod_backup(string)

@app.route("/get_comment/<string>",methods=['GET','POST'])
def get_comment(string):
    return web_tools().get_comment(string)

@app.route("/")
def root():
    return 'api'

@app.route("/above")
def above():
    return {"size": str(web_tools().dir_size()) + 'GB'
            }
'''
#@app.get("/get_danmuku")
'''

if __name__ == '__main__':
    app.run()


