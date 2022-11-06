import datetime
import ormar

from typing import Optional

from db import metadata
from db import database


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=30)


class Project(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=70)
    is_base_project: bool = ormar.Boolean(default=False)
    color: str = ormar.String(max_length=10)


    user: Optional[User] = ormar.ForeignKey(User)


class Task(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=70)
    description: str = ormar.String(max_length=500)
    is_completed: bool = ormar.Boolean(default=False)
    position: int = ormar.Integer()
    priority: int = ormar.Integer()
    datetime_expiration: datetime.datetime = ormar.DateTime()
    datetime_completion: Optional[datetime.datetime] = ormar.DateTime(nullable=True)
    datetime_added: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    project_id: int = ormar.Integer()

    user: Optional[User] = ormar.ForeignKey(User)
    project: Optional[Project] = ormar.ForeignKey(Project)