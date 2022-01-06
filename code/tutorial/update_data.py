# 请求体 - 更新数据

## 用 PUT 更新数据

# 把输入数据转换为以 JSON 格式存储的数据（比如，使用 NoSQL 数据库时），可以使用 jsonable_encoder。
# 例如，把 datetime 转换为 str。
from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

# 注意：当传入的数据不包含已储存的属性时，会使用默认属性覆盖原有属性
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

# 用 PATCH 进行部分更新
# 只发送要更新的数据，其余数据保持不变。


# 使用 Pydantic 的 exclude_unset 参数
# 更新部分数据时，可以在 Pydantic 模型的 .dict() 中使用 exclude_unset 参数
# 比如，item.dict(exclude_unset=True)
# 这段代码生成的 dict 只包含创建 item 模型时显式设置的数据，而不包括默认值
# 然后再用它生成一个只含已设置（在请求中所发送）数据，且省略了默认值的 dict
# 接下来，用 .copy() 为已有模型创建调用 update 参数的副本，该参数为包含更新数据的 dict。
@app.patch("/items/{item_id}", response_model=Item)
async def update_item2(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item

"""简而言之，更新部分数据应：

1. 使用 PATCH 而不是 PUT （可选，也可以用 PUT）；
2. 提取存储的数据；
3. 把数据放入 Pydantic 模型；
4. 生成不含输入模型默认值的 dict （使用 exclude_unset 参数）；
    只更新用户设置过的值，不用模型中的默认值覆盖已存储过的值。
5. 为已存储的模型创建副本，用接收的数据更新其属性 （使用 update 参数）。
6. 把模型副本转换为可存入数据库的形式（比如，使用 jsonable_encoder）。
    这种方式与 Pydantic 模型的 .dict() 方法类似，但能确保把值转换为适配 JSON 的数据类型，例如， 把 datetime 转换为 str 。
7. 把数据保存至数据库；
8. 返回更新后的模型。"""