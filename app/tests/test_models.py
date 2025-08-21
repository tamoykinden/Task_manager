from uuid import UUID
from app.models.task import Task


def test_task_model_creation(db_session):
    """Тест создания модели задачи с сессией БД"""
    task = Task(
        title="Test Task",
        description="Test Description",
        status="created"
    )
    
    db_session.add(task)
    db_session.flush()
    
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "created"
    assert isinstance(task.id, UUID)


def test_task_model_default_status(db_session):
    """Тест значения статуса по умолчанию с сессией БД"""
    task = Task(title="Test", description="Test")
    
    db_session.add(task)
    db_session.flush()
    
    assert task.status == "created"


def test_task_model_without_session():
    """Тест модели без сессии"""
    task = Task(
        title="Test Task",
        description="Test Description",
        status="in_progress"
    )
    
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "in_progress"