from uuid import UUID
import enum
from pydantic import BaseModel, Field
from typing import Optional


class TaskStatus(enum.Enum):
    """Перечисление статусов задачи"""
    created = 'created'
    in_progress = 'in_progress'
    completed = 'completed'

class TaskBase(BaseModel):
    """Схема с общими атрибутами для создания и чтения"""
    title: str = Field(..., min_length = 1, max_length = 100, example = 'Смодерировать архитектуру')
    description = Optional[str] = Field(None, min_length = 1, max_length = 1000, example = 'Написать код для инициализации БД')
    status: Optional[TaskStatus] = Field(default = TaskStatus.created, example = TaskStatus.created)

class TaskCreate(TaskBase):
    """Схема создания задачи"""
    #Наследуются все поля от базовой схемы
    pass

class TaskUpdate(BaseModel):
    """Схема для обновления задачи"""
    #Использую Optional, чтобы можно было любое поле обновлять отдельно
    title: Optional[str] = Field(None, min_length=1, max_length=100, example = 'Обновленное название')
    description = Optional[str] = Field(None, min_length = 1, max_length = 1000, example = 'Обновленное описание')
    status: Optional[TaskStatus] = Field(None, example = TaskStatus.in_progress)

class Task(TaskBase):
    """Схема для чтения и возврата данных о задаче"""
    #Добавляю обязательное поле id
    id: UUID

    class Config:
        #Конфигурация для работы с ORM (чтобы преобразовывать объекты в схему)
        from_attributes = True