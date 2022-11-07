from fastapi import FastAPI

from api import main_router

from sql_app import models
from sql_app.database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(main_router)