from datetime import timedelta

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends

import app.pydantic_schemas.schemas as schemas
import app.db.models as models
import app.dependencies.user as user_dep
import app.dependencies.auth as auth_dep
import app.email_send.email_send as email_send


user_router = APIRouter(tags=['User'])


@user_router.get('/user', response_model=schemas.User)
def get_info_user(current_user: models.User = Depends(auth_dep.get_current_user)):
    return current_user
 

@user_router.post('/user', response_model=schemas.User, response_model_exclude_unset=True)
def add_user(db_user: schemas.User = Depends(user_dep.create_user)):
    return db_user


@user_router.put('/user', response_model=schemas.User)
def update_user(
                user_update: schemas.UserUpdate, 
                current_user: models.User = Depends(auth_dep.get_current_user)
                ):
    user_update_dict = user_update.dict()
    user = user_dep.update_user(current_user.id, **user_update_dict)
    return user


@user_router.get('/code')
def get_change_code(
                    background_tasks: BackgroundTasks,
                    code: int = Depends(auth_dep.create_change_code),
                    currrent_user: models.User = Depends(auth_dep.get_current_user)
                    ):

    background_tasks.add_task(
                            email_send.send_email1, 
                            email=currrent_user.email, 
                            username=currrent_user.username,
                            code=code
                            )
    return code
