from email import message
from typing import Union

from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path

from schemas import User


app = FastAPI()


@app.post('/user')
async def create_user(user: User):
    user_dict = user.dict()
    passlen = len(user.password)
    user_dict.update({'passlen': passlen})
    return user_dict
