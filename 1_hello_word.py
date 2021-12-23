from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CityInfo(BaseModel):
    province: str
    country: str
    in_assfected: Optional[bool] = None

@app.get('/')
def hello_word():
    return {"message": "Hello World"}

@app.get('/city/{city}')
def result(city: str, query_string: Optional[str] = None):
    return {'city': city, 'query_string': query_string}


# 启动命令 uvicorn main:app --reload  # 更改后重载