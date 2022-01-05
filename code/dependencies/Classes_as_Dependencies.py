# 
# 在上一个例子中，我们在依赖函数中返回了一个字典
# 但是随后我们在路径操作函数的参数commons中得到了一个dict
# 并且编辑器会对这个字典提供支持，因为它知道里面的值有什么
from typing import Optional
from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

# 是什么生成了依赖
# 上面的例子中依赖为一个函数，但实际上只要是可调用对象都可以作为依赖项
# 所以，我们可以创建类来作为依赖项
# 我们将 common_parameters 函数更换为了 CommonQueryParams 类
# 并在初始化函数中使用相同的参数

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items2/")
async def read_items2(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

# FastAPI 调用 CommonQueryParams 类。这将创建该类的一个“实例”，并且该实例将作为参数 commons 传递给函数
# 当依赖项为一个类时，可以不用在 Depends() 中声明它，只需要在类型注释中声明就足够了，Fastapi 会知道怎么做
# 像这样，read_items2(commons: CommonQueryParams = Depends())