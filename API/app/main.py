import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import db.models as models
# from actions import get_db
# from api import main_router
from routes.auth import auth_router
from routes.user import user_router
from routes.project import project_router
from routes.task import task_router
from db.database import SessionLocal
from db.database import engine
from config import settings

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