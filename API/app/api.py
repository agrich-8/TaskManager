import shutil
from datetime import datetime
from email import message

from fastapi import APIRouter
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import Form
from fastapi import File
from fastapi import Depends
from fastapi import UploadFile

from sqlalchemy.orm import Session

from schemas import UserIn
from schemas import UserOut
from schemas import ProjectIn
from schemas import ProjectOut
from schemas import TaskOut
from schemas import TaskUpdate

from sql_app import schemas
from sql_app import crud
from sql_app.database import SessionLocal


main_router = APIRouter(prefix='/main',
                        tags=['tasks']
                        )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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



@main_router.post('/taskAdd')
def task_add(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task=task)
    

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


@main_router.put('/taskList')
async def task_list():
    task = await Task.objects.get()
    print(task)
    p = await task.delete()
    return task