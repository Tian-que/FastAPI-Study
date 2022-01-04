# 响应状态码
from fastapi import FastAPI, status

app = FastAPI()


# status_code 将会在响应中返回该状态码
# status_code 也能够接收一个 IntEnum 类型，比如 Python 的 http.HTTPStatus。
@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}

# 可以使用来自 fastapi.status 的便捷变量
@app.post("/items2/", status_code=status.HTTP_201_CREATED)
async def create_item2(name: str):
    return {"name": name}