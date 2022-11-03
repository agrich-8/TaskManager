import shutil

from email import message

from fastapi import APIRouter
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import Form
from fastapi import File
from fastapi import UploadFile

from schemas import User
from schemas import UserIn
from schemas import UserOut
from schemas import Task
from schemas import TaskOut
from schemas import TaskUpdate

main_router = APIRouter()


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

@main_router.get('/tasks')
async def tasks_list():
    return tasks

@main_router.post('/addTask', response_model=TaskOut)
async def info(task: Task):
    task_dict = task.dict()
    task_dict.update({"task_id": len(tasks)})
    tasks[len(tasks)] = task_dict
    return task_dict

@main_router.put('/updateTask')
async def update_task(task: TaskUpdate):
    task_dict = task.dict(exclude_unset=True)
    update_task = tasks[task.task_id]
    for k in task_dict.keys():
        update_task[k] = task_dict[k]
    return tasks