from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()

# 在函数内部，可以直接访问模型对象的所有属性
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# 请求体 + 路径参数 + 查询参数
# 如果在路径中也声明了该参数，它将被用作路径参数
# 如果参数属于单一类型（比如 int、float、str、bool 等）它将被解释为查询参数
# 如果参数的类型被声明为一个 Pydantic 模型，它将被解释为请求体
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result