# 调试
# 你可以在编辑器中连接调试器，例如使用 Visual Studio Code 或 PyCharm。

# 调用 uvicorn
# 在你的 FastAPI 应用中直接导入 uvicorn 并运行：

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)