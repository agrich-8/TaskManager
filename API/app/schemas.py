from datetime import datetime

from pydantic import BaseModel
from pydantic import validator
from pydantic import Field

class UserP(BaseModel):

    id: int
    name: str
    description: str | None = None
    

class UserIn(UserP):

    password: str = Field(..., min_length=6, description='Password must be longer than 6 characters')

class UserOut(UserP):

    passlen: str


class ProjectIn(BaseModel):

    title: str = Field(default=None)
    is_base_project: bool = Field(default=False)
    color: str = Field(default=None)


class ProjectOut(ProjectIn):

    id: int

class TaskIn(BaseModel):

    title: str = Field(title='The name of the task')
    description: str = Field(title='The description of the task')
    position: int = Field(title='')
    priority: int = Field(title='')
    datetime_expiration: datetime = Field(title='Date and time the task was completed')
    project_id: int = Field(title='Project id, for the base project obtained during registration')

class TaskOut(TaskIn):

    id: int
    is_completed: bool
    datetime_completion: datetime | None
    datetime_added: datetime | None



class TaskUpdate(BaseModel):

    title: str | None = None
    description: str | None = None
    position: int | None = None
    priority: int | None = None
    datetime_expiration: datetime | None = None
    project_id: int | None = None

