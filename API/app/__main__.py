import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from actions import get_db
from api import main_router
from sql_app.database import SessionLocal
import models
from sql_app.database import engine
from config import settings

async def get_db_reak():
   with SessionLocal () as s:
      yield s

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# app.dependency_overrides[get_db] = get_db_reak
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run("__main__:app",
                host=settings.server_host,
                port=settings.server_port,
                reload=True
                )