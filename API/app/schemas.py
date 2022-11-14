from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class TaskBase(BaseModel):
    title: str
    description: str
    position: int
    priority: int
    datetime_expiration: datetime    


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int 
    is_completed: bool
    datetime_completion: datetime
    datetime_added: datetime
    user_id: int
    project_id: int

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    title: str
    is_base_project: bool
    color: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    user_id: int
    tasks: list[Task] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description='Password must be longer than 6 characters')


class User(UserBase):
    id: int
    # projects: list[Project] = []
    # tasks: list[Task] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None= Field(None, min_length=6, description='Password must be longer than 6 characters')


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class ErrorData(BaseModel):
    nameerror: str
    
class Detail(BaseModel):
    detail: str