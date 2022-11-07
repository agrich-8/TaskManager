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
    