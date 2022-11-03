from datetime import datetime

from pydantic import BaseModel
from pydantic import validator
from pydantic import Field

class User(BaseModel):

    id: int
    name: str
    description: str | None = None
    

class UserIn(User):

    password: str = Field(..., min_length=6, description='Password must be longer than 6 characters')

class UserOut(User):

    passlen: str



class Task(BaseModel):

    name: str = Field(default=None, title='The name of the task')
    description: str = Field(default=None, title='The description of the task')
    project_id: int = Field(default=None, title='Project id, for the base project obtained during registration')
    datetime_of_complite: datetime = Field(default=None, title='Date and time the task was completed')


class TaskOut(Task):

    task_id: int | None


class TaskUpdate(BaseModel):

    task_id: int 
    name: str = Field(default=None, title='The name of the task')
    description: str = Field(default=None, title='The description of the task')
    project_id: int = Field(default=None, title='Project id, for the base project obtained during registration')
    datetime_of_complite: datetime = Field(default=None, title='Date and time the task was completed')
