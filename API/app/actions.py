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
    exception_409(username=user_dict['username'], email=user_dict['email'])
    print('sdcasdcads')
    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update(user_id: int, username=None, email=None, password=None):
    db = next(get_db())
    user = db.query(models.User).filter(models.User.id == user_id).first()
    exception_409(username=username, email=email)
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


def exception_409(username: str = None, email: str = None):
    if get_user(username=username):
        exception_text = 'A user with the same username already exists'
        exception = HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"{exception_text}"
                        )
        raise exception

    if get_user(email=email):
        exception_text = 'A user with the same email already exists'
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
    

    
def get_tasks(user: schemas.User):
    db = next(get_db())
    return db.query(models.Task).filter(models.Task.user_id == user.id).first()


def create_task(task: schemas.TaskCreate, user_id: int):
    db = next(get_db())
    task = task.dict()
    task['user_id'] = user_id
    db_task = models.Task(**task)
    print(db_task)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
