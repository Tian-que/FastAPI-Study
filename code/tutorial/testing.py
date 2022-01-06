# 可以使用 Pytest 进行测试

# ---------------------------------
# TestClient
from fastapi import FastAPI
# 导入 TestClient
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

# 以与处理请求相同的方式使用 TestClient 对象。
client = TestClient(app)

# 使用断言
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

# ---------------------------------
# 分离测试
# 在实际应用程序中，您可能会将测试放在不同的文件中。
# 而且您的 FastAPI 应用程序也可能由多个文件/模块等组成。

# 假设您的 FastAPI 应用程序有一个 main.py 文件：
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

# 然后你可以有一个包含测试的文件 test_main.py，并从主模块 (main.py) 导入你的应用程序：
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

# ----------------------------------------
# 测试：扩展示例
# 扩展的 FastAPI 应用程序文件
# 假设您有一个包含 FastAPI 应用程序的 main_b.py 文件。
# 它有一个可能返回错误的 GET 操作。
# 它有一个 POST 操作，可能会返回几个错误。
# 两个路径操作都需要一个 X-Token 标头。

from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()


class Item(BaseModel):
    id: str
    title: str
    description: Optional[str] = None


@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id] = item
    return item

# 扩展测试文件

# 然后你可以有一个 test_main_b.py，和以前一样，带有扩展测试
from fastapi.testclient import TestClient

from .main_b import app

client = TestClient(app)


def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}

# 请注意，TestClient 接收可以转换为 JSON 的数据，而不是 Pydantic 模型。
# 如果您的测试中有 Pydantic 模型，并且您想在测试期间将其数据发送到应用程序，则可以使用 JSON Compatible Encoder 中描述的 jsonable_encoder。

# 运行它
# 首先需要安装 pytest
