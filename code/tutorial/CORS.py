# CORS（跨域资源共享）
# CORS 或者「跨域资源共享」 指浏览器中运行的前端拥有与后端通信的 JavaScript 代码，而后端处于与前端不同的「源」的情况。

# 源是协议（http，https）、域（myapp.com，localhost，localhost.tiangolo.com）以及端口（80、443、8080）的组合。
# 因此，这些都是不同的源：
# - http://localhost
# - https://localhost
# - http://localhost:8080
# 即使它们都在 localhost 中，但是它们使用不同的协议或者端口，所以它们都是不同的「源」

# 使用 CORSMiddleware
# 你可以在 FastAPI 应用中使用 CORSMiddleware 来配置它。

# 导入 CORSMiddleware。
# 创建一个允许的源列表（由字符串组成）。
# 将其作为「中间件」添加到你的 FastAPI 应用中。
# 你也可以指定后端是否允许：

# 凭证（授权 headers，Cookies 等）。
# 特定的 HTTP 方法（POST，PUT）或者使用通配符 "*" 允许所有方法。
# 特定的 HTTP headers 或者使用通配符 "*" 允许所有 headers。

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}

# 默认情况下，这个 CORSMiddleware 实现所使用的默认参数较为保守，所以你需要显式地启用特定的源、方法或者 headers，以便浏览器能够在跨域上下文中使用它们。

# 支持以下参数：

# allow_origins - 一个允许跨域请求的源列表。例如 ['https://example.org', 'https://www.example.org']。你可以使用 ['*'] 允许任何源。
# allow_origin_regex - 一个正则表达式字符串，匹配的源允许跨域请求。例如 'https://.*\.example\.org'。
# allow_methods - 一个允许跨域请求的 HTTP 方法列表。默认为 ['GET']。你可以使用 ['*'] 来允许所有标准方法。
# allow_headers - 一个允许跨域请求的 HTTP 请求头列表。默认为 []。你可以使用 ['*'] 允许所有的请求头。Accept、Accept-Language、Content-Language 以及 Content-Type 请求头总是允许 CORS 请求。
# allow_credentials - 指示跨域请求支持 cookies。默认是 False。另外，允许凭证时 allow_origins 不能设定为 ['*']，必须指定源。
# expose_headers - 指示可以被浏览器访问的响应头。默认为 []。
# max_age - 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600。