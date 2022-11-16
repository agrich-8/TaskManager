from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class TaskBase(BaseModel):
    title: str = Field(min_length=1 , max_length=50, description='Title must be no longer than 50 characters')
    description: str = Field(min_length=1 , max_length=500, description='Description must be no longer than 500 characters')
    position: int
    priority: int
    datetime_expiration: datetime




class TaskCreate(TaskBase):
    project_id: int | None = None


class Task(TaskBase):
    id: int 
    is_completed: bool
    datetime_completion: datetime | None
    datetime_added: datetime
    project_id: int
    user_id: int

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    id: int 
    title: str | None = Field(min_length=1 , max_length=50, description='Title must be no longer than 50 characters')
    description: str | None = Field(min_length=1 , max_length=500, description='Description must be no longer than 500 characters')
    position: int | None
    priority: int | None
    datetime_expiration: datetime | None
    is_completed: bool | None
    datetime_completion: datetime | None
    project_id: int | None


class ProjectBase(BaseModel):
    title: str = Field(min_length=1 , max_length=50, description='Title must be no longer than 50 characters')
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
    title: str | None = Field(None, min_length=1 , max_length=50, description='Title must be no longer than 50 characters')
    color: str | None = None


class UserBase(BaseModel):
    username: str = Field(min_length=1 , max_length=30, description='Username must be no longer than 30 characters')
    email: EmailStr = Field(description='user@example.com')


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=33, description='Password must be longer than 6 characters')


class User(UserBase):
    id: int
    projects: list[Project] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str | None =  Field(None, min_length=1 , max_length=30, description='Username must be no longer than 30 characters')
    email: EmailStr | None = Field(None, description='user@example.com')
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