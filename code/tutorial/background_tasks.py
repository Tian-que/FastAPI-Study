# 可以定义在返回响应后运行的后台任务。
# 这对于需要在请求之后发生的操作很有用，但客户端实际上不必在接收响应之前等待操作完成。

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

# FastAPI 将为您创建 BackgroundTasks 类型的对象并将其作为该参数传递
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

# 依赖注入
# 使用 BackgroundTasks 也可以与依赖注入系统一起使用，您可以在多个级别声明 BackgroundTasks 类型的参数：在路径操作函数中、在依赖项中（可靠的）、在子依赖项中等。
from typing import Optional
from fastapi import Depends
def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}