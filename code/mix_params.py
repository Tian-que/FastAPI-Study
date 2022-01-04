from typing import Optional

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None

# 将默认值设置为 None 来将请求体参数声明为可选参数
# 同时也可以使用多个请求体参数
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: Optional[str] = None,
    item: Optional[Item] = None,
    user: User
):
    results = {"item_id": item_id, "user": user}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# 请求体中的单一值
# 可以使用 Body 指示 FastAPI 将其作为请求体的另一个键进行处理
@app.put("/items2/{item_id}")
async def update_item2(
    item_id: int, item: Item, user: User, importance: int = Body(...)
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

# 嵌入单个请求体参数
# 这样可以要求在 json 中 指明 "item":{} 而不是 {}
@app.put("/items3/{item_id}")
async def update_item3(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
