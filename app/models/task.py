from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid
from app.database import Base

class TaskStatus(enum.Enum):
    """Перечисление статусов задачи"""
    created = 'created'
    in_progress = 'in_progress'
    completed = 'completed'

class Task(Base):
    """Модель для задач"""
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(Text, max_length=1000,nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.created)

