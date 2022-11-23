import app.db.models as models
import app.pydantic_schemas.schemas as schemas
from .db import get_db
from .exception import exception_409_user
from .project import create_project

def get_user(username: str = None, email: str = None):
    db = next(get_db())
    user = None
    if username:
        user = db.query(models.User).filter(models.User.username == username).first()
    if email:
        user = db.query(models.User).filter(models.User.email == email).first()
    return user


def create_user(user: schemas.UserCreate):
    db = next(get_db())
    user_dict = user.dict()
    print(user_dict)
    exception_409_user(username=user_dict['username'], email=user_dict['email'])
    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    primary_project_dict = {
                "is_base_project": True,
                "title": "Base",
                "color": "string"
                }
    project = schemas.ProjectPrimary(**primary_project_dict)
    create_project(project, db_user.id)
    return db_user


def update_user(user_id: int, username=None, email=None, password=None):
    db = next(get_db())
    user = db.query(models.User).filter(models.User.id == user_id).first()
    exception_409_user(username=username, email=email)
    if username:
        user.username = username        
    if email:
        user.email = email
    if password:
        user.password = password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user