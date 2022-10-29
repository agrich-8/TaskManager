from datetime import date

from pydantic import BaseModel
from pydantic import validator
from pydantic import Field

class User(BaseModel):

    id: int
    name: str
    password: str = Field(..., min_length=6, description='Password must be longer than 6 characters')
    description: str | None = None