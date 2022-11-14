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
from actions import get_db
# from sql_app.database import SessionLocal


main_router = APIRouter(prefix='/main',
                        tags=['tasks']
                        )


@main_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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


@main_router.get('/user', response_model=schemas.User)
def info_user(current_user: models.User = Depends(actions.get_current_user)):
    return current_user
 

@main_router.post('/user', response_model=schemas.User, response_model_exclude_unset=True)
def add_user(user: schemas.UserCreate):
    db_user = actions.create_user(user)
    return db_user


@main_router.put('/user')
def update_user(update: schemas.UserUpdate, current_user: models.User = Depends(actions.get_current_user)):
    update = update.dict()
    user = actions.update(current_user.id, **update)
    return user


@main_router.get('/tasks')
def info_tasks(current_user: schemas.User = Depends(actions.get_current_user)):
    tasks = actions.get_tasks(current_user)
    return tasks


@main_router.post('/task')
def add_task(
            task: schemas.TaskCreate,
            current_user: schemas.User = Depends(actions.get_current_user)
            ):
    db_task = actions.create_task(task=task, user_id=current_user.id)
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