# 使用密码和 Bearer 的简单 OAuth2

# 获取 username 和 password
# 我们将使用 FastAPI 的安全性实用工具来获取 username 和 password

from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status

# 导入 OAuth2PasswordRequestForm，然后在 token 的路径操作中通过 Depends 将其作为依赖项使用
# OAuth2PasswordRequestForm 是一个类依赖项，声明了如下的请求表单：
# - username。
# - password。
# - 一个可选的 scope 字段，是一个由空格分隔的字符串组成的大字符串。
# - 一个可选的 grant_type.
# - 一个可选的 client_id（我们的示例不需要它）。
# - 一个可选的 client_secret（我们的示例不需要它）。
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


# 更新依赖项
# 现在我们将更新我们的依赖项。
# 我们想要仅当此用户处于启用状态时才能获取 current_user。
# 因此，我们创建了一个额外的依赖项 get_current_active_user，而该依赖项又以 get_current_user 作为依赖项。
# 如果用户不存在或处于未启用状态，则这两个依赖项都将仅返回 HTTP 错误。
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            
            # 我们在此处返回的值为 Bearer 的额外响应头 WWW-Authenticate 也是规范的一部分。
            # 任何的 401「未认证」HTTP（错误）状态码都应该返回 WWW-Authenticate 响应头。
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 现在，使用表单字段中的 username 从（伪）数据库中获取用户数据。
    # 如果没有这个用户，我们将返回一个错误消息，提示「用户名或密码错误」。
    # 对于这个错误，我们使用 HTTPException 异常：
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # 返回令牌
    # token 端点的响应必须是一个 JSON 对象
    # 它应该有一个 token_type。在我们的例子中，由于我们使用的是「Bearer」令牌，因此令牌类型应为「bearer」
    # 并且还应该有一个 access_token 字段，它是一个包含我们的访问令牌的字符串
    # 对于这个简单的示例，我们将极其不安全地返回相同的 username 作为令牌
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


