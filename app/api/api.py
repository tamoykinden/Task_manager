from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.crud.task import TaskService
from app.database import get_db

logger = logging.getLogger(__name__)

class TaskAPIRouter:
    """Класс для организации API роутов задач"""
    
    def __init__(self):
        self.router = APIRouter()
        self._register_routes()
    
    def _register_routes(self):
        """Регистрация всех роутов"""
        
        @self.router.post('/', response_model=Task, status_code=status.HTTP_201_CREATED)
        def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
            """Создать новую задачу"""
            try:
                service = TaskService(db)
                return service.create_task(task)
            except SQLAlchemyError as e:
                logger.error(f"Database error in create task: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error while creating task"
                )
            except Exception as e:
                logger.error(f"Unexpected error in create task: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected error occurred"
                )
        
        @self.router.get('/', response_model=List[Task])
        def read_task_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
            """Получить список всех задач с пагинацией"""
            try:
                service = TaskService(db)
                tasks = service.get_tasks(skip=skip, limit=limit)
                return tasks
            except SQLAlchemyError as e:
                logger.error(f"Database error in get tasks list: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error while fetching tasks"
                )
            except Exception as e:
                logger.error(f"Unexpected error in get tasks list: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected error occurred"
                )
        
        @self.router.get("/{task_id}", response_model=Task)
        def read_one_task(task_id: UUID, db: Session = Depends(get_db)):
            """Получить задачу по UUID"""
            try:
                service = TaskService(db)
                db_task = service.get_task(task_id=task_id)
                
                if db_task is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found"
                    )
                return db_task
            except HTTPException:
                # Пробрасываю HTTPException как есть (404 ошибки)
                raise
            except SQLAlchemyError as e:
                logger.error(f"Database error in get task {task_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error while fetching task"
                )
            except Exception as e:
                logger.error(f"Unexpected error in get task {task_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected error occurred"
                )
        
        @self.router.patch("/{task_id}", response_model=Task)
        def update_existing_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
            """Обновить существующую задачу"""
            try:
                service = TaskService(db)
                db_task = service.update_task(task_id=task_id, task_update=task_update)
                
                if db_task is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found"
                    )
                return db_task
            except HTTPException:
                raise
            except SQLAlchemyError as e:
                logger.error(f"Database error in update task {task_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error while updating task"
                )
            except Exception as e:
                logger.error(f"Unexpected error in update task {task_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected error occurred"
                )
        
        @self.router.delete("/{task_id}", response_model=Task)
        def delete_existing_task(task_id: UUID, db: Session = Depends(get_db)):
            """Удалить задачу"""
            try:
                service = TaskService(db)
                db_task = service.delete_task(task_id=task_id)
                
                if db_task is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found"
                    )
                return db_task
            except HTTPException:
                raise
            except SQLAlchemyError as e:
                logger.error(f"Database error in delete task {task_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error while deleting task"
                )
            except Exception as e:
                logger.error(f"Unexpected error in delete task {task_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected error occurred"
                )


# Создаю экземпляр роутера
task_router = TaskAPIRouter()
router = task_router.router