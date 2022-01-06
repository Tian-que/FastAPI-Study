# 上下文管理器依赖项

# FastAPI 支持在完成后执行一些额外步骤的依赖项
# 为此，请使用 yield 而不是 return，并在后面写下额外的步骤

# 和 Python 中使用 yield 生成上下文管理器一样

# 具有 yield 的数据库依赖项
# 例如，可以使用它来创建一个数据库会话并在完成后关闭它。
# 产生的值是注入到路径操作和其他依赖项中的值
# yield 语句后面的代码在响应传递后
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

# 使用 yield 和 try 的依赖
# 如果在依赖项中使用 try 块和 yield，将会收到使用依赖项时抛出的任何异常
# 可以使用 except SomeException 在依赖项中查找该特定异常
# 同样，可以使用 finally 来确保执行退出步骤，无论是否有异常。


# 使用 yield 的子依赖
# FastAPI 将确保每个依赖项中的“退出代码”以正确的顺序运行。
# 例如，dependency_c 可以依赖dependency_b，dependency_b 可以依赖dependency_a
# 它们会以调用栈的形式逐个退出，并且在每个依赖项中执行正确的退出代码。

from fastapi import Depends


async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)


# 具有 yield 和 HTTPException 的依赖项
# 下面这一堆话的核心就是如果需要更改响应或对用户侧抛出异常一定要在 yield 语句之前丢出去，否则异常不会被传给用户


# 在 yield 之后，在退出代码中引发 HTTPException 或类似的异常可能很诱人。但它不会工作。
# 带有 yield 的依赖项中的退出代码在 Exception Handlers 之后执行。退出代码中没有捕获依赖项引发的异常
# 因此，如果在 yield 之后引发 HTTPException，则捕获 HTTPExceptions 并返回 HTTP 400 响应的默认（或任何自定义）异常处理程序将不再用于捕获该异常。
# 着允许在依赖项中设置的任何内容（例如数据库会话），例如，被后台任务使用。
# 后台任务在响应发送后运行。因此无法引发 HTTPException，因为甚至无法更改已发送的响应。
# 但是，如果后台任务创建了数据库错误，至少可以回滚或干净地关闭依赖项中的会话，并可以记录错误或将其报告给远程跟踪系统。
# 如果知道某些代码可能引发异常，请执行最正常的 Pythonic 操作并在该部分代码中添加一个 try 块。
# 如果想在返回响应之前处理自定义异常并可能修改响应，甚至可能引发 HTTPException，请创建自定义异常处理程序。


# 仍然可以在 yield 之前引发异常，包括 HTTPException。但不是之后


# 同样可以在依赖中使用上下文管理器
# 妈的，又套娃
class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

# 依赖项中的退出代码可以使用上下文管理器，而不是使用 try/finally。
async def get_db():
    with MySuperContextManager() as db:
        yield db