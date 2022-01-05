# 全局依赖项

# 有时，我们要为整个应用添加依赖项。
# 通过与定义路径装饰器依赖项 类似的方式，可以把依赖项添加至整个 FastAPI 应用。
# 这样一来，就可以为所有路径操作应用该依赖项

from fastapi import Depends, FastAPI, Header, HTTPException


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]