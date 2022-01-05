# 使用 FastAPI 提供的工具来处理安全性

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# 当我们创建 OAuth2PasswordBearer 类的实例时，我们传入 tokenUrl 参数。
# 此参数包含客户端（在用户浏览器中运行的前端）将用于发送用户名和密码以获取令牌的 URL。
# 这里的 tokenUrl="token" 指的是我们还没有创建的相对 URL 标记。因为它是一个相对 URL，所以它相当于 ./token。
# 因为我们使用的是相对 URL，如果您的 API 位于 https://example.com/，那么它将引用 https://example.com/token。
# 但是，如果您的 API 位于 https://example.com/api/v1/，那么它将引用 https://example.com/api/v1/token。

# oauth2_scheme 变量是 OAuth2PasswordBearer 的一个实例，但它也是一个 callable 。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 此依赖项将提供一个 str，该 str 分配给路径操作函数的参数 token 。
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# FastAPI 提供了几种不同抽象级别的工具来实现这些安全功能
# 在这个例子中，我们将使用 OAuth2，使用密码流，使用 Bearer token。我们使用 OAuth2PasswordBearer 类来做到这一点。