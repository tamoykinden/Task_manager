import pytest
from uuid import uuid4
from pydantic import ValidationError
from app.schemas.task import TaskCreate, TaskUpdate, Task


def test_task_create_schema_valid():
    """Тест валидной схемы создания задачи"""
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "created"
    }
    
    task = TaskCreate(**task_data)
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "created"


def test_task_create_schema_minimal():
    """Тест схемы создания задачи с минимальными данными"""
    task_data = {
        "title": "Test Task"
    }
    
    task = TaskCreate(**task_data)
    assert task.title == "Test Task"
    assert task.description is None
    assert task.status == "created" 


def test_task_create_schema_default_status():
    """Тест значения по умолчанию для статуса"""
    task_data = {
        "title": "Test Task",
        "description": "Test Description"
    }
    
    task = TaskCreate(**task_data)
    assert task.status == "created"  


def test_task_create_schema_invalid_title():
    """Тест невалидного названия задачи"""
    with pytest.raises(ValidationError):
        TaskCreate(title="") 
    
    with pytest.raises(ValidationError):
        TaskCreate(title="A" * 101)  


def test_task_create_schema_invalid_description():
    """Тест невалидного описания"""
    with pytest.raises(ValidationError):
        TaskCreate(title="Test", description="")  
    
    with pytest.raises(ValidationError):
        TaskCreate(title="Test", description="A" * 1001)  


def test_task_create_schema_invalid_status():
    """Тест невалидного статуса"""
    with pytest.raises(ValidationError):
        TaskCreate(title="Test", status="invalid_status")  


def test_task_update_schema_valid():
    """Тест валидной схемы обновления задачи"""
    update_data = {
        "title": "Updated Title",
        "status": "in_progress"
    }
    
    task_update = TaskUpdate(**update_data)
    assert task_update.title == "Updated Title"
    assert task_update.status == "in_progress"
    assert task_update.description is None


def test_task_update_schema_partial():
    """Тест частичного обновления"""
    # Только название
    update1 = TaskUpdate(title="New Title")
    assert update1.title == "New Title"
    assert update1.description is None
    assert update1.status is None
    
    # Только статус
    update2 = TaskUpdate(status="completed")
    assert update2.title is None
    assert update2.description is None
    assert update2.status == "completed"
    
    # Только описание
    update3 = TaskUpdate(description="New Description")
    assert update3.title is None
    assert update3.description == "New Description"
    assert update3.status is None


def test_task_update_schema_empty():
    """Тест пустого обновления"""
    update = TaskUpdate()
    assert update.title is None
    assert update.description is None
    assert update.status is None


def test_task_schema_valid():
    """Тест основной схемы задачи"""
    task_id = uuid4()
    task_data = {
        "id": task_id,
        "title": "Test Task",
        "description": "Test Description",
        "status": "created"
    }
    
    task = Task(**task_data)
    assert task.id == task_id
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "created"


def test_task_schema_from_attributes():
    """Тест преобразования из атрибутов (для ORM)"""
    task_id = uuid4()
    task_data = {
        "id": task_id,
        "title": "Test Task",
        "description": "Test Description",
        "status": "in_progress"
    }
    
    task = Task.model_validate(task_data)
    assert task.id == task_id
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "in_progress"


def test_task_schema_missing_required():
    """Тест отсутствия обязательных полей"""
    with pytest.raises(ValidationError):
        Task() 
    
    with pytest.raises(ValidationError):
        Task(id=uuid4())  
    
    with pytest.raises(ValidationError):
        Task(title="Test") 


def test_task_schema_optional_fields():
    """Тест опциональных полей"""
    task_id = uuid4()
    
    task1 = Task(id=task_id, title="Test Task", status="created")
    assert task1.description is None
    
    task2 = Task(
        id=task_id,
        title="Test Task", 
        description="Test Description",
        status="completed"
    )
    assert task2.description == "Test Description"


def test_task_status_values():
    """Тест допустимых значений статуса"""
    TaskCreate(title="Test", status="created")
    TaskCreate(title="Test", status="in_progress")
    TaskCreate(title="Test", status="completed")
    
    with pytest.raises(ValidationError):
        TaskCreate(title="Test", status="invalid")


def test_task_schema_serialization():
    """Тест сериализации в JSON"""
    task_id = uuid4()
    task = Task(
        id=task_id,
        title="Test Task",
        description="Test Description",
        status="created"
    )
    
    task_dict = task.model_dump()
    assert task_dict["id"] == task_id
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == "Test Description"
    assert task_dict["status"] == "created"
    
    task_json = task.model_dump_json()
    assert str(task_id) in task_json
    assert "Test Task" in task_json