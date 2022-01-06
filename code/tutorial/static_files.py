# 静态文件
# 可以使用 StaticFiles 从目录中自动提供静态文件。

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 挂载一个静态文件目录
# 第一个 static 为路由目录
# 第二个为本地目录
# 第三个为可由内部调用的名称
app.mount("/static", StaticFiles(directory="static"), name="static")