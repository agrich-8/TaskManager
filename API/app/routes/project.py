from fastapi import APIRouter
from fastapi import Depends

import pydantic_schemas.schemas as schemas
import db.models as models
import dependencies.auth as auth_dep
import dependencies.project as project_dep


project_router = APIRouter(tags=['Project'])


@project_router.get('/project', response_model=schemas.Project | list[schemas.Project])
def info_project(
                project_id: int | None = None, 
                base: bool | None = None,
                current_user: models.User = Depends(auth_dep.get_current_user)
                ):
    projects = project_dep.get_project(project_id=project_id, user_id=current_user.id, base=base)
    return projects


@project_router.post('/project', response_model=schemas.Project)
def add_project(
                project: schemas.ProjectCreate, 
                current_user: models.User = Depends(auth_dep.get_current_user)
                ):
    db_project = project_dep.create_project(project=project, user_id=current_user.id)
    return db_project


@project_router.put('/project', response_model=schemas.Project)
def update_project(
                    project_update: schemas.ProjectUpdate, 
                    current_user: models.User = Depends(auth_dep.get_current_user)
                    ):
    project_update_dict = project_update.dict()
    project = project_dep.update_project(user_id=current_user.id, **project_update_dict)
    return project


@project_router.delete('/project', response_model=schemas.Project)
def delete_project(
                project_id: int,
                current_user: models.User = Depends(auth_dep.get_current_user)
                ):
    project = project_dep.delete_project(project_id=project_id, user_id=current_user.id)
    return project
