from typing import List, Optional

from fastapi import FastAPI, Query

app = FastAPI()

# 使用 Query 进行参数校验
# 使用正则表达式校验 
# ^ 以该符号之后的字符开头，符号之前没有字符。
# fixedquery: 值精确地等于 fixedquery
# $: 到此结束，在 fixedquery 之后没有更多字符
# 如果在使用 Query 且需要声明一个值为必须时，可以使用 "..." 代替 "None"
@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# 查询参数列表 / 多个值
@app.get("/items2/")
async def read_items(q: Optional[List[str]] = Query(
    ["foo", "bar"], 
    title="Query string", 
    description="Query string for the items to search in the database that have a good match")
    ):
    query_items = {"q": q}
    return query_items

# 别名参数
# 使用 alias 来指定一个在 Python 中非法的路径名
# http://127.0.0.1:8000/items/?item-query=foobaritems
@app.get("/items3/")
async def read_items(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# 弃用参数
# 将参数 deprecated=True 传入 Query
@app.get("/items4/")
async def read_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results