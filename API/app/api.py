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
from fastapi.security import OAuth2PasswordRequestForm

import schemas
import models
import actions
import config


main_router = APIRouter(prefix='/main',
                        tags=['tasks']
                        )


@main_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = actions.authenticate_user(form_data.username, form_data.password)
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

# @main_router.post('/uploadImg')
# async def upload_img(file: list[UploadFile] = File(..., description="Profile picture")):
#     for file in file:
#         with open(f'{file.filename}', 'wb') as f:
#             shutil.copyfileobj(file.file, f)
#     return {'filename': file.filename}


@main_router.get('/user', response_model=schemas.User)
def info_user(current_user: models.User = Depends(actions.get_current_user)):
    return current_user
 

@main_router.post('/user', response_model=schemas.User, response_model_exclude_unset=True)
def add_user(db_user: schemas.User = Depends(actions.create_user)):
    return db_user


@main_router.put('/user', response_model=schemas.User)
def update_user(
                user_update: schemas.UserUpdate, 
                current_user: models.User = Depends(actions.get_current_user)
                ):
    user_update_dict = user_update.dict()
    user = actions.update_user(current_user.id, **user_update_dict)
    return user


@main_router.get('/project', response_model=schemas.Project)
def info_project(
                project_id: int | None = None, 
                base: bool | None = None,
                current_user: models.User = Depends(actions.get_current_user)
                ):
    projects = actions.get_project(project_id=project_id, user_id=current_user.id, base=base)
    return projects


@main_router.post('/project', response_model=schemas.Project)
def add_project(
                project: schemas.ProjectCreate, 
                current_user: models.User = Depends(actions.get_current_user)
                ):
    db_project = actions.create_project(project=project, user_id=current_user.id)
    return db_project


@main_router.put('/project', response_model=schemas.Project)
def update_project(
                    project_update: schemas.ProjectUpdate, 
                    current_user: models.User = Depends(actions.get_current_user)
                    ):
    project_update_dict = project_update.dict()
    project = actions.update_project(user_id=current_user.id, **project_update_dict)
    return project


@main_router.get('/task', response_model=schemas.Task)
def info_task(
                task_id: int | None = None,
                current_user: schemas.User = Depends(actions.get_current_user)
                ):
    tasks = actions.get_tasks(task_id=task_id, user_id=current_user.id)
    return tasks


@main_router.post('/task', response_model=schemas.Task)
def add_task(
            task: schemas.TaskCreate,
            current_user: schemas.User = Depends(actions.get_current_user)
            ):
    db_task = actions.create_task(task=task, user_id=current_user.id)
    return db_task
    

@main_router.put('/task', response_model=schemas.Task)
def update_task(
                    task_update: schemas.TaskUpdate, 
                    current_user: models.User = Depends(actions.get_current_user)
                    ):
    task_update_dict = task_update.dict()
    task = actions.update_task(user_id=current_user.id, **task_update_dict)
    return task