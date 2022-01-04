# 模式的额外信息 - 例子
from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

# 使用 Config 与 schema_extra 
# 在 Field, Path, Query, Body 以及之后将会看到的工厂函数可以为 JSON 模式声明额外信息，也可以通过给工厂函数传递其他的任意参数来给JSON 模式声明额外信息
# 传递的那些额外参数不会添加任何验证，只会添加注释，用于文档的目的。
class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

# Body 额外参数
# 可以通过传递额外信息给 Field 同样的方式操作 Path, Query, Body等
@app.put("/items2/{item_id}")
async def update_item2(
    item_id: int,
    item: Item = Body(
        ...,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results