# 处理错误
from fastapi import FastAPI, HTTPException


app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

# 添加自定义响应头
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            # 使用自定义响应头
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}

# 安装自定义异常处理器
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

# 它返回如下内容 {"message": "Oops! yolo did something. There goes a rainbow..."}
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

# 请求 /unicorns/yolo 时，路径操作会触发 UnicornException
# 该异常将会被 unicorn_exception_handler 处理
@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

# 覆盖默认异常处理器
"""
FastAPI 自带了一些默认异常处理器。
触发 HTTPException 或请求无效数据时，这些处理器返回默认的 JSON 响应结果。
不过，也可以使用自定义处理器覆盖默认异常处理器。
"""
# 覆盖请求验证异常
# 请求中包含无效数据时，FastAPI 内部会触发 RequestValidationError
# 覆盖默认异常处理器时需要导入 RequestValidationError
# 并用 @app.excption_handler(RequestValidationError) 装饰异常处理器

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

# 覆盖 HTTPException 错误处理器
# 同理，也可以覆盖 HTTPException 处理器
# 例如，只为错误返回纯文本响应，而不是返回 JSON 格式的内容
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.get("/items4/{item_id}")
async def read_item4(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

# 使用 RequestValidationError 的请求体
# RequestValidationError 包含其接收到的无效数据请求的 body
# 开发时，可以用这个请求体生成日志、调试错误，并返回给用户
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

# FastAPI 也提供了自有的 HTTPException
# FastAPI 的 HTTPException 继承自 Starlette 的 HTTPException 错误类。
# 它们之间的唯一区别是，FastAPI 的 HTTPException 可以在响应中添加响应头
# 注册异常处理器时，应该注册到来自 Starlette 的 HTTPException


# 复用 FastAPI 异常处理器
# FastAPI 支持先对异常进行某些处理，然后再使用 FastAPI 中处理该异常的默认异常处理器。
# 从 fastapi.exception_handlers 中导入要复用的默认异常处理器
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException



@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}