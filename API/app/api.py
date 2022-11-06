import shutil
from datetime import datetime
from email import message

from fastapi import APIRouter
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import Form
from fastapi import File
from fastapi import UploadFile

from schemas import UserIn
from schemas import UserOut
from schemas import ProjectIn
from schemas import ProjectOut
from schemas import TaskIn
from schemas import TaskOut
from schemas import TaskUpdate

from models import User
from models import Project
from models import Task

main_router = APIRouter(prefix='/main',
                        tags=['tasks']
                        )


tasks = {}


@main_router.post('/user', response_model=UserOut)
async def create_user(user: UserIn):
    
    user_dict = user.dict()
    passlen = len(user.password)
    user_dict.update({'passlen': passlen})
    return user_dict


@main_router.post('/uploadImg')
async def upload_img(file: list[UploadFile] = File(..., description="Profile picture")):
    for file in file:
        with open(f'{file.filename}', 'wb') as f:
            shutil.copyfileobj(file.file, f)
    return {'filename': file.filename}


@main_router.post('/projectAdd', response_model=ProjectOut)
async def add_project(project: ProjectIn):
    project_dict = project.dict()
    print(project_dict)
    project_save = Project(**project_dict)
    saved_project = await project_save.save()
    return saved_project


@main_router.post('/taskAdd', response_model=TaskOut)
async def info(task: TaskIn):
    task_dict = task.dict()
    task_save = Task(**task_dict)
    print(task_dict)
    saved_task = await task_save.save()
    return saved_task
    

@main_router.put('/taskUpdate', response_model=TaskOut)
async def task_update(*, task_id: int = Query(ge=0), task: TaskUpdate):
    task_dict = task.dict(exclude_unset=True)
    task = await Task.objects.get(id=task_id)
    print(task)
    p = await task.update(**task_dict)
    return p


@main_router.put('/taskCompleted')
async def task_complete(task_id: int = Query(ge=0)):
    task = await Task.objects.get(id=task_id)
    print(task)
    p = await task.update(is_completed=True, datetime_completion=datetime.now())
    return p


@main_router.put('/taskDelete') #@@@@@@@@@@@@@__delete__@@@@@@@@@@@@@@@
async def task_delete(task_id: int = Query(ge=0)):
    task = await Task.objects.get(id=task_id)
    print(task)
    p = await task.delete()
    return task


# @main_router.put('/taskList')
# async def task_list():
#     task = await Task.objects.get()
#     print(task)
#     p = await task.delete()
#     return task