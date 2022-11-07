from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def create_task(db: Session, task: schemas.TaskCreate):
    task = task.dict()
    db_task = models.Task(**task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

    