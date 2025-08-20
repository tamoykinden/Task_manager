from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from schemas.task import Task
from crud.task import TaskCreate, TaskUpdate , create_task, get_tasks, get_task, update_task, delete_task
from database import get_db


from app import crud, schemas

#Создаю роутер
router = APIRouter

@router.post('/', response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Создать задачу"""
    return create_task(task=task, db=db)

@router.get('/', response_model=Task)
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех задач с пагинацией"""
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model = Task)
def read_task(task_id: UUID, db: Session = Depends(get_db)):
    """Получить задачу по UUID"""
    db_task = get_task(db, task_id = task_id)
    # Если задача не найдена, возвращаем ошибку
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task

@router.patch("/{task_id}", response_model = Task)
def update_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Обновить задачу"""
    db_task = update_task(db, task_id = task_id, task_update = task_update)
    if db_task is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Task not found"
        )
    return db_task

@router.delete("/{task_id}", response_model = Task)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    """Удалить задачу"""
    db_task = delete_task(db, task_id = task_id)
    if db_task is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Task not found"
        )
    return db_task
