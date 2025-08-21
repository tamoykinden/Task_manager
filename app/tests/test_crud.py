import pytest
from uuid import UUID
from app.crud.task import TaskService
from app.schemas.task import TaskCreate, TaskUpdate


def test_create_task(task_service, sample_task_data):
    """Тест создания задачи через сервис"""
    task_create = TaskCreate(**sample_task_data)
    task = task_service.create_task(task_create)
    
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "created"


def test_get_task(task_service, sample_task_data):
    """Тест получения задачи по ID"""
    task_create = TaskCreate(**sample_task_data)
    created_task = task_service.create_task(task_create)
    
    retrieved_task = task_service.get_task(created_task.id)
    
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Test Task"


def test_get_nonexistent_task(task_service):
    """Тест получения несуществующей задачи"""
    task = task_service.get_task(UUID("00000000-0000-0000-0000-000000000000"))
    assert task is None


def test_get_tasks_list(task_service):
    """Тест получения списка задач"""
    # Создаем несколько задач
    for i in range(3):
        task_data = TaskCreate(
            title=f"Task {i}", 
            description=f"Description {i}",
            status="created"
        )
        task_service.create_task(task_data)
    
    tasks = task_service.get_tasks()
    
    assert len(tasks) == 3
    assert tasks[0].title == "Task 0"
    assert tasks[1].title == "Task 1"


def test_update_task(task_service, sample_task_data):
    """Тест обновления задачи"""
    task_create = TaskCreate(**sample_task_data)
    created_task = task_service.create_task(task_create)
    
    update_data = TaskUpdate(title="Updated Title", status="in_progress")
    updated_task = task_service.update_task(created_task.id, update_data)
    
    assert updated_task.title == "Updated Title"
    assert updated_task.status == "in_progress"
    assert updated_task.description == "Test Description"  # Не изменилось


def test_delete_task(task_service, sample_task_data):
    """Тест удаления задачи"""
    task_create = TaskCreate(**sample_task_data)
    created_task = task_service.create_task(task_create)
    
    deleted_task = task_service.delete_task(created_task.id)
    should_be_none = task_service.get_task(created_task.id)
    
    assert deleted_task.id == created_task.id
    assert should_be_none is None


def test_update_partial(task_service, sample_task_data):
    """Тест частичного обновления задачи"""
    task_create = TaskCreate(**sample_task_data)
    created_task = task_service.create_task(task_create)
    
    # Обновляем только статус
    update_data = TaskUpdate(status="completed")
    updated_task = task_service.update_task(created_task.id, update_data)
    
    assert updated_task.status == "completed"
    assert updated_task.title == "Test Task"  # Не изменилось
    assert updated_task.description == "Test Description"  # Не изменилось


def test_pagination(task_service):
    """Тест пагинации списка задач"""
    # Создаем 5 задач
    for i in range(5):
        task_data = TaskCreate(
            title=f"Task {i}", 
            description=f"Description {i}",
            status="created"
        )
        task_service.create_task(task_data)
    
    # Получаем первые 2 задачи
    tasks = task_service.get_tasks(skip=0, limit=2)
    assert len(tasks) == 2
    assert tasks[0].title == "Task 0"
    assert tasks[1].title == "Task 1"
    
    # Пропускаем первые 2, получаем следующие 2
    tasks = task_service.get_tasks(skip=2, limit=2)
    assert len(tasks) == 2
    assert tasks[0].title == "Task 2"
    assert tasks[1].title == "Task 3"