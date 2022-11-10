import shutil
from datetime import datetime
from datetime import timedelta
from email import message

from fastapi import APIRouter
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import Form
from fastapi import File
from fastapi import Depends
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

import schemas
import models
import actions
import config
from sql_app.database import SessionLocal


main_router = APIRouter(prefix='/main',
                        tags=['tasks']
                        )


@main_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(actions.get_db)):
    print('sdcasdcasdcadsc')
    user = actions.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = actions.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@main_router.post('/uploadImg')
async def upload_img(file: list[UploadFile] = File(..., description="Profile picture")):
    for file in file:
        with open(f'{file.filename}', 'wb') as f:
            shutil.copyfileobj(file.file, f)
    return {'filename': file.filename}


@main_router.get('/user')
def info_user(token: str, db: Session = Depends(actions.get_db)):
    user = actions.get_current_user(db, token)
    return {"token": user}


@main_router.post('/user')
def add_user(user: schemas.UserCreate):
    try:
        db_user = actions.create_user(user)
    except NameError:
        return {"NameError": 'User already exists'}
    return db_user


@main_router.post('/user_ccc')
def userccc(user: schemas.UserCreate, db: Session = Depends(actions.get_db)):
    user_dict = user.dict()
    db_user = actions.get_user(db, user_dict['username'])
    ver = db_user.verify_password(user_dict['password'])
    return ver


@main_router.get('/task')
def info_user(token: str):
    user = actions.get_task(token)
    return {"token": user}


@main_router.post('/task')
def add_task(task: schemas.TaskCreate):
    db_task = actions.create_task(task=task)
    return db_task
    
    
# @main_router.put('/taskUpdate', response_model=TaskOut)
# async def task_update(*, task_id: int = Query(ge=0), task: TaskUpdate):
#     task_dict = task.dict(exclude_unset=True)
#     task = await Task.objects.get(id=task_id)
#     print(task)
#     p = await task.update(**task_dict)
#     return p


# @main_router.put('/taskCompleted')
# async def task_complete(task_id: int = Query(ge=0)):
#     task = await Task.objects.get(id=task_id)
#     print(task)
#     p = await task.update(is_completed=True, datetime_completion=datetime.now())
#     return p


# @main_router.put('/taskDelete') #@@@@@@@@@@@@@__delete__@@@@@@@@@@@@@@@
# async def task_delete(task_id: int = Query(ge=0)):
#     task = await Task.objects.get(id=task_id)
#     print(task)
#     p = await task.delete()
#     return task


# @main_router.put('/taskList')q
# async def task_list():
#     task = await Task.objects.get()
#     print(task)
#     p = await task.delete()
#     return task