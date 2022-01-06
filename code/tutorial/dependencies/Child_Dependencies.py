# FastAPI 支持创建含子依赖项的依赖项
# 可以按需声明任意深度的子依赖项嵌套层级
from typing import Optional
from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: Optional[str] = None):
    return q

# 该函数声明了类型是 str 的可选 cookie（last_query）,
# 用户未提供查询参数 q 时，则使用上次使用后保存在 cookie 中的查询
def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}

# 注意，这里在路径操作函数中只声明了一个依赖项，即 query_or_cookie_extractor 。
# 但 FastAPI 必须先处理 query_extractor，以便在调用 query_or_cookie_extractor 时使用 query_extractor 返回的结果。

# 多次使用同一个依赖项
# 如果在同一个路径操作 多次声明了同一个依赖项，例如，多个依赖项共用一个子依赖项，FastAPI 在处理同一请求时，只调用一次该子依赖项。
# FastAPI 不会为同一个请求多次调用同一个依赖项，而是把依赖项的返回值进行「缓存」，并把它传递给同一请求中所有需要使用该返回值的「依赖项」
# 在高级使用场景中，如果不想使用「缓存」值，而是为需要在同一请求的每一步操作（多次）中都实际调用依赖项，可以把 Depends 的参数 use_cache 的值设置为 False
async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
    return {"fresh_value": fresh_value}