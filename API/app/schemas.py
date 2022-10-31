from datetime import date

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