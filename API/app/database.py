from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings
import config

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
# def SessionLocal():
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # return SessionLocal

Base = declarative_base()