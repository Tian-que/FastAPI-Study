# 中间件
"""
你可以向 FastAPI 应用添加中间件.

"中间件"是一个函数,它在每个请求被特定的路径操作处理之前,以及在每个响应返回之前工作.

它接收你的应用程序的每一个请求.
然后它可以对这个请求做一些事情或者执行任何需要的代码.
然后它将请求传递给应用程序的其他部分 (通过某种路径操作).
然后它获取应用程序生产的响应 (通过某种路径操作).
它可以对该响应做些什么或者执行任何需要的代码.
然后它返回这个 响应.
"""

# 如果你使用了 yield 关键字依赖, 依赖中的退出代码将在执行中间件后执行.
# 如果有任何后台任务(稍后记录), 它们将在执行中间件后运行.

# 创建中间件
# 要创建中间件你可以在函数的顶部使用装饰器 @app.middleware("http").

# 中间件参数接收如下参数:

# - request.
# - 一个函数 call_next 它将接收 request 作为参数.
# -     这个函数将 request 传递给相应的 路径操作.
# -     然后它将返回由相应的路径操作生成的 response.
# - 然后你可以在返回 response 前进一步修改它.

# 请记住可以 用'X-' 前缀添加专有自定义请求头.

# 但是如果你想让浏览器中的客户端看到你的自定义请求头, 你需要把它们加到 CORS 配置 (CORS (Cross-Origin Resource Sharing)) 
# 的 expose_headers 参数中,在 Starlette's CORS docs文档中.

import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 感觉和装饰器差不多