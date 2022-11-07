from datetime import datetime

from pydantic import BaseModel


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
    password: str


class User(UserBase):
    id: int
    projects: list[Project] = []
    tasks: list[Task] = []

    class Config:
        orm_mode = True