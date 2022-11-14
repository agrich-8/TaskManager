from datetime import timedelta
from datetime import datetime

from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from sqlalchemy.orm import Session
# from main import SessionLocal

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

import models
import schemas
import config
from sql_app.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="main/token")

# def get_db():
#     raise NotImplementedError

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    exception_409_user(username=user_dict['username'], email=user_dict['email'])
    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    project_dict = {
                "is_base_project": True,
                "title": "Base",
                "color": "string"
                }
    project = schemas.ProjectPrimary(**project_dict)
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


def exception_409_user(username: str = None, email: str = None):
    if get_user(username=username):
        exception_text = 'User with the same username already exists'
        exception = HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"{exception_text}"
                        )
        raise exception

    if get_user(email=email):
        exception_text = 'User with the same email already exists'
        exception = HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"{exception_text}"
                        )
        raise exception


def authenticate_user(db: Session, username: str, password: str):
    print('sdfvsdfvsdfvsdfvsdfvsdfvsdfv')
    print(username, password)
    user = get_user(username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
    

def get_project(
                user_id: int, 
                project_id: int | None = None, 
                base: bool | None = None, 
                limit: int = 20
                ):
    db = next(get_db())
    if base:
        return db.query(models.Project).filter(models.Project.user_id == user_id, models.Project.is_base_project == base).first()
    if project_id:
        return db.query(models.Project).filter(models.Project.user_id == user_id, models.Project.id == project_id).first()
    return db.query(models.Project).filter(models.Project.user_id == user_id).limit(limit).all()


def create_project(project: schemas.ProjectCreate|schemas.ProjectPrimary, user_id: int):
    db = next(get_db())    
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
    db = next(get_db())
    project = db.query(models.Project).filter(models.User.id == user_id, models.Project.id == id).first()   
    if title:
        project.title = title
    if color:
        project.color = color
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_tasks(task_id: int, user_id: int, limit: int = 50):
    db = next(get_db())    
    if task_id:
        return db.query(models.Task).filter(models.Task.user_id == user_id, models.Task.id == task_id).first()
    return db.query(models.Task).filter(models.Task.user_id == user_id).limit(limit).all()


def create_task(task: schemas.TaskCreate, user_id: int):
    db = next(get_db())
    projects = [p.id for p in get_project(user_id=user_id)]
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
    
    db = next(get_db())
    exception = HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="The user has no specified projects"
                        )
    task = db.query(models.Task).filter(models.User.id == user_id, models.Task.id == id).first()   
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
        projects = [p.id for p in get_project(user_id=user_id)]
        if project_id not in projects:
            raise exception
        task.project_id = project_id

    db.add(task)
    db.commit()
    db.refresh(task)
    return task