import sqlalchemy

import pydantic_schemas.schemas as schemas
import db.models as models
import dependencies.db as db_f
import dependencies.task as task

from .exception import exception_409

def get_project(
                user_id: int, 
                project_id: int | None = None, 
                base: bool | None = None, 
                limit: int = 20
                ):
    db = next(db_f.get_db())
    if base is True:
        return db.query(models.Project).filter(models.Project.user_id == user_id, models.Project.is_base_project == base).first()
    if project_id:
        return db.query(models.Project).filter(models.Project.id == project_id).first()
    return db.query(models.Project).filter(models.Project.user_id == user_id).limit(limit).all()


def create_project(project: schemas.ProjectCreate|schemas.ProjectPrimary, user_id: int):
    db = next(db_f.get_db())
    project_dict = project.dict()
    project_dict['user_id'] = user_id
    db_project = models.Project(**project_dict)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(
                    user_id: int, 
                    id: int,
                    title: str = None, 
                    color: str = None
                    ):
    db = next(db_f.get_db())
    project = db.query(models.Project).filter(models.User.id == user_id, models.Project.id == id).first()
    if project is None:
        exception_409(exception_text='The user has no specified project')
    if title:
        project.title = title
    if color:
        project.color = color
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def delete_project(project_id: int, user_id: int):
    db = next(db_f.get_db())
    try:
        tasks = db.query(models.Task).filter(models.User.id == user_id, models.Task.project_id == project_id).all()
        for t in tasks:
            task.delete_task(task_id=t.id, user_id=user_id)
        project = db.query(models.Project).filter(models.User.id == user_id, models.Project.id == project_id).first()
        db.delete(project)
        db.commit()
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        raise exception_409(exception_text='The user has no specified project')
    return project
