from email import message
from typing import Union

from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import Form
from fastapi import File
from fastapi import UploadFile

from schemas import User
from schemas import UserIn
from schemas import UserOut


app = FastAPI()


@app.post('/user', response_model=UserOut)
async def create_user(user: UserIn):
    
    user_dict = user.dict()
    passlen = len(user.password)
    user_dict.update({'passlen': passlen})
    return user_dict

@app.post('file')
async def file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}