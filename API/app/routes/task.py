from fastapi import APIRouter
from fastapi import Depends

import pydantic_schemas.schemas as schemas
import db.models as models
import dependencies.auth as auth_dep
import dependencies.task as task_dep


task_router = APIRouter(tags=['Task'])



@task_router.get('/task', response_model=schemas.Task)
def info_task(
            task_id: int | None = None,
            current_user: schemas.User = Depends(auth_dep.get_current_user)
            ):
    tasks = task_dep.get_tasks(task_id=task_id, user_id=current_user.id)
    return tasks


@task_router.post('/task', response_model=schemas.Task)
def add_task(
            task: schemas.TaskCreate,
            current_user: schemas.User = Depends(auth_dep.get_current_user)
            ):
    db_task = task_dep.create_task(task=task, user_id=current_user.id)
    return db_task
    

@task_router.put('/task', response_model=schemas.Task)
def update_task(
                task_update: schemas.TaskUpdate, 
                current_user: models.User = Depends(auth_dep.get_current_user)
                ):
    task_update_dict = task_update.dict()
    task = task_dep.update_task(user_id=current_user.id, **task_update_dict)
    return task


@task_router.delete('/task', response_model=schemas.Task)
def delete_task(
                task_id: int,
                current_user: models.User = Depends(auth_dep.get_current_user)
                ):
    task = task_dep.delete_task(task_id=task_id, user_id=current_user.id)
    return task

