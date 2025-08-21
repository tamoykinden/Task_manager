from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    """Схема с общими атрибутами для создания и чтения"""
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    status: Optional[str] = Field(default='created')

class TaskCreate(TaskBase):
    """Схема создания задачи"""
    pass

class TaskUpdate(BaseModel):
    """Схема для обновления задачи"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    status: Optional[str] = Field(None)

class Task(TaskBase):
    """Схема для чтения и возврата данных о задаче"""
    id: UUID

    class Config:
        from_attributes = True