# 上一节中，基于依赖项注入系统的）安全系统向路径操作函数提供了一个 str 类型的 token

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# 但这还不是很实用，让我们来使它返回当前用户给我们。

# 创建一个用户模型
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = 
    
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

# get_current_user 将具有一个我们之前所创建的同一个 oauth2_scheme 作为依赖项
# 依赖项 get_current_user 将从子依赖项 oauth2_scheme 中接收一个 str 类型的 token
# get_current_user 将使用我们创建的（伪）工具函数，该函数接收 str 类型的令牌并返回我们的 Pydantic User 模型
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

