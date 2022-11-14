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
    project_id: int | None = None


class Task(TaskBase):
    id: int 
    is_completed: bool
    datetime_completion: datetime
    datetime_added: datetime
    project_id: int
    user_id: int

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    id: int 
    title: str | None 
    description: str | None
    position: int | None
    priority: int | None
    datetime_expiration: datetime | None
    is_completed: bool | None
    datetime_completion: datetime | None
    project_id: int | None


class ProjectBase(BaseModel):
    title: str
    color: str


class ProjectPrimary(ProjectBase):
    is_base_project: bool = True


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    is_base_project: bool = False
    user_id: int
    tasks: list[Task] = []

    class Config:
        orm_mode = True

class ProjectUpdate(BaseModel):
    id: int 
    title: str | None = None
    color: str | None = None


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