import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from passlib.context import CryptContext


from .database import Base


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)

    projects = relationship('Project', back_populates='user', passive_deletes=True, lazy='subquery')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute') 

    @password.setter
    def password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.hashed_password)

    def get_password_hash(self, password: str):
        return pwd_context.hash(password)


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    is_base_project = Column(Boolean, default=False)
    color = Column(String)
    is_favorite = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='projects', passive_deletes=True, lazy='subquery')
    tasks = relationship('Task', back_populates='project', passive_deletes=True, lazy='subquery')



class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    position = Column(Integer)
    priority = Column(Integer)
    section = Column(String)
    datetime_expiration = Column(DateTime)
    datetime_completion = Column(DateTime, nullable=True)
    datetime_added = Column(DateTime, default=datetime.datetime.now)
    project_id = Column(Integer, ForeignKey('projects.id'))

    project = relationship('Project', back_populates='tasks', passive_deletes=True, lazy='subquery')

