from sqlalchemy.orm import Session
from uuid import UUID
from app import schemas
from models.task import Task
from schemas.task import TaskCreate

def get_task(db: Session, task_id: UUID):
    """Функция ддля получения одной задачи"""
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db:Session, skip: int=0, limit: int=100):
    """Функция для получения нескольких задач"""
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db:Session, task: TaskCreate):
    """Функция для создания задачи"""
    #распаковка словаря с данными
    db_task = Task(**task.dict())
    #Добавляю объект в БД
    db.add(db_task)
    db.commit()
    #обновление объекта
    db.refresh(db_task)
    return db_task

