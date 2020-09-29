from fastapi import FastAPI

app = FastAPI()#创建app对象

@app.get("/{name}")#返回静态内容
def read_root(name):
    return {"Hello": "World" + name}

@app.get("/items/{item_id}")#含有查询内容
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("")