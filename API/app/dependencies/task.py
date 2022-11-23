from datetime import datetime

import sqlalchemy
from fastapi import HTTPException
from fastapi import status

import app.pydantic_schemas.schemas as schemas
import app.db.models as models
import app.dependencies.project as project 
import app.dependencies.db as db_f
from .exception import exception_409


def get_tasks(task_id: int, user_id: int, limit: int = 50):
    db = next(db_f.get_db())    
    if task_id:
        return db.query(models.Task).filter(models.Task.user_id == user_id, models.Task.id == task_id).first()
    return db.query(models.Task).filter(models.Task.user_id == user_id).limit(limit).all()


def create_task(task: schemas.TaskCreate, user_id: int):
    db = next(db_f.get_db())
    projects = [p.id for p in project.get_project(user_id=user_id)]
    exception = HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="The user has no specified projects"
                        )
    if task.project_id is None:
        base_project = db.query(models.Project).filter(models.Project.user_id == user_id, models.Project.is_base_project == True).first()
        task.project_id = base_project.id

    if task.project_id not in projects:
        raise exception

    task_dict = task.dict()
    task_dict['user_id'] = user_id
    db_task = models.Task(**task_dict)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(user_id: int,
                id: int,
                title: str | None = None,
                description: str | None = None,
                position: int | None = None,
                priority: int | None = None,
                datetime_expiration: datetime | None = None,
                is_completed: bool | None = None,
                datetime_completion: datetime | None = None,
                project_id: int | None = None, 
                # **kwargs
                ):

    # for key, vol in kwargs.items():
    # d = dict(filter(lambda x:x[1], kwargs.items()))
    # print(d)
    
    db = next(db_f.get_db())
    exception = HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="The user has no specified projects"
                        )
    
    task = db.query(models.Task).filter(models.User.id == user_id, models.Task.id == id).first()   
    if task is None:
        raise exception
    if id:
        task.id = id
    if title:
        task.title = title
    if description:
        task.description = description
    if position:
        task.position = position
    if priority:
        task.priority = priority
    if datetime_expiration:
        task.datetime_expiration = datetime_expiration
    if is_completed:
        task.is_completed = is_completed # add setter
    if datetime_completion:
        task.datetime_completion = datetime_completion
    if project_id:
        project = project.get_project(user_id=user_id, project_id=project_id)
        if project is None:
            exception_409(exception_text='The user has no specified projects')
        task.project_id = project_id

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(task_id: int, user_id: int):
    db = next(db_f.get_db())
    exception = HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="The user has no specified task"
                    )
    try:
        task = db.query(models.Task).filter(models.User.id == user_id, models.Task.id == task_id).first()
        db.delete(task)
        db.commit()
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        raise exception
    return task

