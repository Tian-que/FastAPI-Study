from typing import Optional, List


from fastapi import Cookie, Header, FastAPI


app = FastAPI()

# Cookie
# 声明 Cookie 参数的结构与声明 Query 参数和 Path 参数时相同
# 第一个值是参数的默认值，同时也可以传递所有验证参数或注释参数，来校验参数
@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}

# Header
# Header 拥有额外的“自动转换”功能
# 默认情况下, Header 将把参数名称的字符从下划线 (_) 转换为连字符 (-) 来提取并记录 headers.
# 同时，HTTP headers 是大小写不敏感的，因此，因此可以使用标准Python样式(也称为 "snake_case")声明它们。
# 因此，可以像通常在Python代码中那样使用 user_agent ，而不需要将首字母大写为 User_Agent 或类似的东西。
# 如果出于某些原因，需要禁用下划线到连字符的自动转换，设置Header的参数 convert_underscores 为 False:
@app.get("/items2/")
async def read_items2(
    strange_header: Optional[str] = Header(None, convert_underscores=False)
):
    return {"strange_header": strange_header}

# 重复的 headers
# 可以通过一个Python list 的形式获得重复header的所有值
@app.get("/items3/")
async def read_items3(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}