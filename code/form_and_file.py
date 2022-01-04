# 表单数据
# 接收的不是 JSON，而是表单字段时，要使用 Form
# pip install python-multipart
from fastapi import FastAPI, Form

app = FastAPI()

# 使用 Form 可以声明与 Body （及 Query、Path、Cookie）相同的元数据和验证
# Form 是直接继承自 Body 的类。
# 声明表单体要显式使用 Form ，否则，FastAPI 会把该参数当作查询参数或请求体（JSON）参数
# 表单数据的「媒体类型」编码一般为 application/x-www-form-urlencoded
# 可在一个路径操作中声明多个 Form 参数，但不能同时声明要接收 JSON 的 Body 字段。
# 因为此时请求体的编码是 application/x-www-form-urlencoded，不是 application/json。
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

# 请求文件
from fastapi import File, UploadFile

# 创建文件（File）参数的方式与 Body 和 Form 一样
# File 是直接继承自 Form 的类
# 声明文件体必须使用 File，否则，FastAPI 会把该参数当作查询参数或请求体（JSON）参数
# 如果把路径操作函数参数的类型声明为 bytes，FastAPI 将以 bytes 形式读取和接收文件内容。
# 这种方式把文件的所有内容都存储在内存里，适用于小型文件。
@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# 不过，很多情况下，UploadFile 更好用
# UploadFile 与 bytes 相比有更多优势：
# 1. 使用 spooled 文件：存储在内存的文件超出最大上限时，FastAPI 会把文件存入磁盘
# 2. 这种方式更适于处理图像、视频、二进制文件等大型文件，好处是不会占用所有内存
# 3. 可获取上传文件的元数据
# 4. 自带 file-like async 接口
# 5. 暴露的 Python SpooledTemporaryFile 对象，可直接传递给其他预期「file-like」对象的库。
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

"""
UploadFile 的属性如下：

filename：上传文件名字符串（str），例如， myimage.jpg；
content_type：内容类型（MIME 类型 / 媒体类型）字符串（str），例如，image/jpeg；
file： SpooledTemporaryFile（ file-like 对象）。其实就是 Python文件，可直接传递给其他预期 file-like 对象的函数或支持库。
UploadFile 支持以下 async 方法，（使用内部 SpooledTemporaryFile）可调用相应的文件方法。

write(data)：把 data （str 或 bytes）写入文件；
read(size)：按指定数量的字节或字符（size (int)）读取文件内容；
seek(offset)：移动至文件 offset （int）字节处的位置；
例如，await myfile.seek(0) 移动到文件开头；
执行 await myfile.read() 后，需再次读取已读取内容时，这种方法特别好用；
close()：关闭文件。
因为上述方法都是 async 方法，要搭配「await」使用。
"""

# 多文件上传
# FastAPI 支持同时上传多个文件
# 可用同一个「表单字段」发送含多个文件的「表单数据」。
# 上传多个文件时，要声明含 bytes 或 UploadFile 的列表（List）
from typing import List
from fastapi.responses import HTMLResponse

@app.post("/files2/")
async def create_files2(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles2/")
async def create_upload_files2(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# FastAPI 支持同时使用 File 和 Form 定义文件和表单字段。
# 可在一个路径操作中声明多个 File 与 Form 参数，但不能同时声明要接收 JSON 的 Body 字段。
# 因为此时请求体的编码为 multipart/form-data，不是 application/json。
@app.post("/files3/")
async def create_file3(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
