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
        
        @self.router.post(
            '/', 
            response_model = Task, 
            status_code = status.HTTP_201_CREATED,
            summary = 'Создать новую задачу',
            description = """
            Создает новую задачу в системе.
        
            Параметры:
            - title: Название задачи (обязательное, 1-100 символов)
            - description: Описание задачи (опциональное, до 1000 символов)
            - status: Статус задачи (по умолчанию: "created")
        
            Доступные статусы:
            - created - задача создана
            - in_progress - задача в работе
            - completed - задача завершена                
            """
        )
        def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
            """Создать новую задачу"""
            try:
                service = TaskService(db)
                return service.create_task(task)
            except SQLAlchemyError as e:
                logger.error(f"Database error in create task: {str(e)}")
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = "Internal server error while creating task"
                )
            except Exception as e:
                logger.error(f"Unexpected error in create task: {str(e)}")
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = "Unexpected error occurred"
                )
        
        @self.router.get(
            '/', 
            response_model = List[Task],
            summary = 'Получить список задач',
            description = """
            Возвращает список задач с поддержкой пагинации.
        
            Параметры запроса:
            - skip: Количество задач to skip (по умолчанию: 0)
            - limit: Максимальное количество задач to return (по умолчанию: 100)
        
            Пример:
            `GET /tasks/?skip=0&limit=10` - первые 10 задач
            """
        )
        def read_task_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
            """Получить список всех задач с пагинацией"""
            try:
                service = TaskService(db)
                tasks = service.get_tasks(skip=skip, limit=limit)
                return tasks
            except SQLAlchemyError as e:
                logger.error(f"Database error in get tasks list: {str(e)}")
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error while fetching tasks"
                )
            except Exception as e:
                logger.error(f"Unexpected error in get tasks list: {str(e)}")
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = "Unexpected error occurred"
                )
        
        @self.router.get(
            "/{task_id}", 
            response_model = Task,
            summary= 'Получить задачу по UUID',
            description = """
            Возвращает задачу по указанному UUID.
        
            Параметры пути:
            - task_id: UUID задачи
            
            Ошибки:
            - 404 Not Found - если задача не найдена
            """
        )
        def read_one_task(task_id: UUID, db: Session = Depends(get_db)):
            """Получить задачу по UUID"""
            try:
                service = TaskService(db)
                db_task = service.get_task(task_id=task_id)
                
                if db_task is None:
                    raise HTTPException(
                        status_code = status.HTTP_404_NOT_FOUND,
                        detail = "Task not found"
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
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = "Unexpected error occurred"
                )
        
        @self.router.patch(
            "/{task_id}", 
            response_model = Task,
            summary = 'Обновить задачу',
            description = """
            Частично обновляет данные задачи.
        
            Параметры пути:
            - task_id: UUID задачи для обновления
        
            Тело запроса (опциональные поля):
            - title: Новое название задачи
            - description: Новое описание задачи
            - status: Новый статус задачи
        
            Особенности:
            - Обновляются только переданные поля
            - Остальные поля остаются неизменными
        
            Ошибки:
            - 404 Not Found - если задача не найдена
            """
        )
        def update_existing_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
            """Обновить существующую задачу"""
            try:
                service = TaskService(db)
                db_task = service.update_task(task_id=task_id, task_update=task_update)
                
                if db_task is None:
                    raise HTTPException(
                        status_code = status.HTTP_404_NOT_FOUND,
                        detail = "Task not found"
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
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = "Unexpected error occurred"
                )
        
        @self.router.delete(
            "/{task_id}", 
            response_model=Task,
            summary='Удалить задачу',
            description="""
            Удаляет задачу по указанному UUID.
        
            Параметры пути:
            - task_id: UUID задачи для удаления
        
            Особенности:
            - Задача полностью удаляется из системы
            - Операция необратима
        
            Ошибки:
            - 404 Not Found - если задача не найдена
        
            Возвращает:
            Удаленную задачу (последнее состояние перед удалением).
            """
        )
        def delete_existing_task(task_id: UUID, db: Session = Depends(get_db)):
            """Удалить задачу"""
            try:
                service = TaskService(db)
                db_task = service.delete_task(task_id = task_id)
                
                if db_task is None:
                    raise HTTPException(
                        status_code = status.HTTP_404_NOT_FOUND,
                        detail = "Task not found"
                    )
                return db_task
            except HTTPException:
                raise
            except SQLAlchemyError as e:
                logger.error(f"Database error in delete task {task_id}: {str(e)}")
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = "Internal server error while deleting task"
                )
            except Exception as e:
                logger.error(f"Unexpected error in delete task {task_id}: {str(e)}")
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = "Unexpected error occurred"
                )


# Создаю экземпляр роутера
task_router = TaskAPIRouter()
router = task_router.router