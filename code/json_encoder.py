# json 兼容编码器
# 在某些情况下，您可能需要将数据类型（如 Pydantic 模型）转换为与 JSON 兼容的类型（如字典、列表等）
# FastAPI 提供了一个 jsonable_encoder() 函数
# 它接收一个对象，如 Pydantic 模型，并返回一个 JSON 兼容版本

from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


app = FastAPI()

# 使用 jsonable_encoder 转换 Pydantic 模型为 JSON 
# 调用结果可以用 Python 标准 json.dumps() 编码。
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data