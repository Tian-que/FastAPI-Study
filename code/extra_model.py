# 额外的模型
# 一般而言
# 输入模型需要拥有密码属性
# 输出模型不应该包含密码
# 数据库模型很可能需要保存密码的哈希值
# 我们应当根据它们的密码字段以及使用位置去定义模型

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    # 解包 dict 和额外关键字
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# Union 或者 anyOf
# 可以将一个响应声明为两种类型的 Union，这意味着该响应将是两种类型中的任何一种
from typing import Union

class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items2/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item2(item_id: str):
    return items[item_id]

# 模型列表
# 可以用同样的方式声明由对象列表构成的响应
from typing import List
class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/items3/", response_model=List[Item])
async def read_items3():
    return items