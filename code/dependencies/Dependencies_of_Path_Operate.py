# 路径操作装饰器依赖项
# 有时，我们并不需要在路径操作函数中使用依赖项的返回值。
# 或者说，有些依赖项不返回值。
# 但仍要执行或解析该依赖项。
# 对于这种情况，不必在声明路径操作函数的参数时使用 Depends，而是可以在路径操作装饰器中添加一个由 dependencies 组成的 list。

# 在路径操作装饰器中添加 dependencies 参数
# 路径操作装饰器支持可选参数 ~ dependencies。
# 该参数的值是由 Depends() 组成的 list
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

# 路径操作装饰器依赖项（以下简称为“路径装饰器依赖项”）的执行或解析方式和普通依赖项一样
# 但就算这些依赖项会返回值，它们的值也不会传递给路径操作函数。
# 依赖项是可复用的，只是路径操作装饰器不对其进行处理而已，如果是路径操作函数则会对其正常响应
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

