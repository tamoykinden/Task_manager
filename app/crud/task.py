from sqlalchemy.orm import Session
from uuid import UUID
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def get_task(db: Session, task_id: UUID):
    """Функция ддля получения одной задачи"""
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db:Session, skip: int=0, limit: int=100):
    """Функция для получения нескольких задач"""
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db:Session, task: TaskCreate):
    """Функция для создания задачи"""
    #распаковка словаря с данными
    db_task = Task(**task.model_dump())
    #Добавляю объект в БД
    db.add(db_task)
    db.commit()
    #обновление объекта
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: UUID, task_update: TaskUpdate):
    """Функция для обновления задачи"""
    #Ищу задачу, которую нужно обновить
    db_task = get_task(db, task_id)
    if db_task:
        update_data = task_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            #устанавливаем новое значение атрибуту объекта
            setattr(db_task, field, value)

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

    return db_task

def delete_task(db: Session, task_id: UUID):
    """Функция удаления задачи"""
    #Нахожу задачу
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()

    # Возвращаем удаленный объект (или None, если не нашли)
    return db_task

