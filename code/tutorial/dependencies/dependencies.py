"""
什么是「依赖注入」¶
编程中的「依赖注入」是声明代码（本文中为路径操作函数 ）运行所需的，或要使用的「依赖」的一种方式。

然后，由系统（本文中为 FastAPI）负责执行任意需要的逻辑，为代码提供这些依赖（「注入」依赖项）。

依赖注入常用于以下场景：

1. 共享业务逻辑（复用相同的代码逻辑）
2. 共享数据库连接
3. 实现安全、验证、角色权限
...
上述场景均可以使用依赖注入，将代码重复最小化。
"""
# 创建依赖项
# 依赖项就是一个函数，且可以使用与路径操作函数相同的参数
from typing import Optional
from fastapi import Depends, FastAPI
app = FastAPI()


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# 声明依赖项
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


"""
其他与「依赖注入」概念相同的术语为：

* 资源（Resource）
* 提供方（Provider）
* 服务（Service）
* 可注入（Injectable）
* 组件（Component）
"""

# FastAPI 插件
