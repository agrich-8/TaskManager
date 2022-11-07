import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, max_length=30)
    email = Column(String, max_length=50)
    hashed_password = Column(String)

    projects = relationship('Project', back_populates='user')
    tasks = relationship('Task', back_populates='user')
    

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String, max_length=70)
    is_base_project = Column(Boolean, default=False)
    color = Column(String, max_length=10)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='projects')
    tasks = relationship('Task', back_populates='project')



class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, max_length=70)
    description = Column(String, max_length=500)
    is_completed = Column(Boolean, default=False)
    position = Column(Integer)
    priority = Column(Integer)
    datetime_expiration = Column(DateTime)
    datetime_completion = Column(DateTime, nullable=True)
    datetime_added = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))

    user = relationship('User', back_populates='tasks')
    project = relationship('Project', back_populates='tasks')