from typing import Optional

from fastapi import FastAPI, Path, Query

app = FastAPI()

# 路径参数总是必须的
# 所以需要将其标记为 ... ，但即使不标记 Fastapi 也会将其设为必须
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 按需对参数排序
# 这部分和 Python 的关键字参数规范相同
# 如果需要规定所有参数均为关键字参数可以将第一个参数设为 " * "
@app.get("/items2/{item_id}")
async def read_items2(
    q: str, item_id: int = Path(..., title="The ID of the item to get")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 数值校验
# gt：大于（greater than）
# ge：大于等于（greater than or equal）
# lt：小于（less than）
# le：小于等于（less than or equal）
@app.get("/items3/{item_id}")
async def read_items(
    *, item_id: int = Path(..., title="The ID of the item to get", ge=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results