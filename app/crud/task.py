from sqlalchemy.orm import Session
from uuid import UUID
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class TaskService:
    """Сервис для работы с задачами"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_task(self, task_id: UUID) -> Task | None:
        """Получить задачу по ID"""
        try:
            return self.db.query(Task).filter(Task.id == task_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting task {task_id}: {str(e)}")
            raise
    
    def get_tasks(self, skip: int = 0, limit: int = 100) -> list[Task]:
        """Получить список задач с пагинацией"""
        try:
            return self.db.query(Task).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting tasks list: {str(e)}")
            raise
    
    def create_task(self, task: TaskCreate) -> Task:
        """Создать новую задачу"""
        try:
            db_task = Task(**task.model_dump())
            self.db.add(db_task)
            self.db.commit()
            self.db.refresh(db_task)
            return db_task
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error creating task: {str(e)}")
            raise
    
    def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Task | None:
        """Обновить существующую задачу"""
        try:
            db_task = self.get_task(task_id)
            if db_task:
                update_data = task_update.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(db_task, field, value)
                self.db.commit()
                self.db.refresh(db_task)
            return db_task
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error updating task {task_id}: {str(e)}")
            raise
    
    def delete_task(self, task_id: UUID) -> Task | None:
        """Удалить задачу"""
        try:
            db_task = self.get_task(task_id)
            if db_task:
                self.db.delete(db_task)
                self.db.commit()
            return db_task
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error deleting task {task_id}: {str(e)}")
            raise