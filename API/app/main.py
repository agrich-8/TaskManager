import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from .db import models
# import db.models as models
# from actions import get_db
# from api import main_router
from app.routes.auth import auth_router
from app.routes.user import user_router
from app.routes.project import project_router
from app.routes.task import task_router
from app.db.database import SessionLocal
from app.db.database import engine
from app.config import settings

async def get_db_reak():
   with SessionLocal () as s:
      yield s

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(project_router)


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.server_host,
                port=settings.server_port,
                reload=True
                )