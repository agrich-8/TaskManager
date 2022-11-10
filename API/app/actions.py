from datetime import timedelta
from datetime import datetime

from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

import models
import schemas
import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="main/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(user: schemas.UserCreate):
    db = next(get_db())
    user_dict = user.dict()
    if get_user(user_dict['username']):
        raise NameError('User already exists')

    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(username: str):
    db = next(get_db())
    return db.query(models.User).filter(models.User.username == username).first()


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
    

    
def get_task(task_id: int):
    db = next(get_db())
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(task: schemas.TaskCreate):
    db = next(get_db())
    task = task.dict()
    db_task = models.Task(**task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task