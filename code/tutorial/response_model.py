# 响应模型
# 可以在任意的路径操作中使用 response_model 参数来声明用于响应的模型
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []

# FastAPI 将使用此 response_model 来：
# 1. 将输出数据转换为其声明的类型
# 2. 校验数据
# 3. 在 OpenAPI 的路径操作中为响应添加一个 JSON Schema
# 4. 在自动生成文档系统中使用
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item

# 最重要的是它会将输出数据限制在该模型定义内。下面我们会看到这一点有多重要
# 返回与输入相同的数据
# 现在，每当浏览器使用一个密码创建用户时，API 都会在响应中返回相同的密码
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

# 我们正在使用此模型声明输入数据，并使用同一模型声明输出数据
@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn):
    return user

# 添加输出模型
# 我们可以创建一个有明文密码的输入模型和一个没有明文密码的输出模型
# 现在即可对同一组数据指定不同的输入输出模型
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

@app.post("/user2/", response_model=UserOut)
async def create_user2(user: UserIn):
    return user

# 响应模型编码参数
# 响应模型可以具有默认值
class Item2(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
# 可以设置路径操作装饰器的 response_model_exclude_unset=True 来屏蔽认值的字段输出
@app.get("/items/{item_id}", response_model=Item2, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]

# 还可以使用路径操作装饰器的 response_model_include 和 response_model_exclude 参数
# 它们接收一个由属性名称 str 组成的 set 来包含（忽略其他的）或者排除（包含其他的）这些属性
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]

# 使用 list 而不是 set
# 如果忘记使用 set 而是使用 list 或 tuple，FastAPI 仍会将其转换为 set 并且正常工作
# 例如这样 response_model_include=["name", "description"]