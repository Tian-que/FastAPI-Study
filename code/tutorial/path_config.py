# 路径操作
# 可以将几个参数传递给路径操作装饰器

# 响应状态码
from typing import Optional, Set

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []

# 直接响应 HTTP_201_CREATED
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

# 标签，可以使用str列表来表示标签，这些内容将会反馈在文档上
@app.post("/items2/", response_model=Item, tags=["items"])
async def create_item2(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]

# 总结和描述
# Summary and description
@app.post(
    "/items3/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item3(item: Item):
    return item

# 来自文档字符串的描述
@app.post("/items4/", response_model=Item, summary="Create an item")
async def create_item4(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# 响应描述
@app.post(
    "/items5/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item5(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# 弃用 Deprecate 
# 这将会在文档中标注
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]