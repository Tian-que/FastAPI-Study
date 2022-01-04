from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
app = FastAPI()

# 关于这玩意，我只能说套娃真好玩
class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    # 可以在model里面套娃字段检查，参数同 Query，Path
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
