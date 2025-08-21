import pytest
from fastapi import status
from uuid import UUID


def test_create_task(client, sample_task_data):
    """Тест создания задачи через API"""
    response = client.post("/tasks/", json=sample_task_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    
    assert data["title"] == sample_task_data["title"]
    assert data["description"] == sample_task_data["description"]
    assert data["status"] == sample_task_data["status"]
    assert "id" in data


def test_get_task(client, created_task):
    """Тест получения задачи через API"""
    task_id = created_task["id"]
    response = client.get(f"/tasks/{task_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"


def test_get_nonexistent_task(client):
    """Тест получения несуществующей задачи"""
    response = client.get("/tasks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"


def test_get_tasks_list(client):
    """Тест получения списка задач"""
    # Создаем несколько задач
    for i in range(3):
        client.post("/tasks/", json={
            "title": f"Task {i}",
            "description": f"Description {i}",
            "status": "created"
        })
    
    response = client.get("/tasks/?skip=0&limit=10")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 3
    assert data[0]["title"] == "Task 0"
    assert data[1]["title"] == "Task 1"


def test_update_task(client, created_task):
    """Тест обновления задачи через API"""
    task_id = created_task["id"]
    
    update_data = {
        "title": "Updated Title",
        "status": "in_progress"
    }
    
    response = client.patch(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "in_progress"
    assert data["description"] == "Test Description"  # Не изменилось


def test_delete_task(client, created_task):
    """Тест удаления задачи через API"""
    task_id = created_task["id"]
    
    # Удаляем задачу
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == status.HTTP_200_OK
    
    # Пытаемся получить удаленную задачу
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_validation_errors(client):
    """Тест валидации входных данных"""
    # Слишком длинное название
    response = client.post("/tasks/", json={
        "title": "A" * 101,  # > 100 символов
        "description": "Test"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY