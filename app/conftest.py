import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.config import TEST_DSN
from app.database import Base, get_db
from main import app


engine = create_engine(
    TEST_DSN,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Создает свежую сессию БД для каждого теста"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Создает тестовый клиент с переопределенной зависимостью БД"""
    
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def task_service(db_session):
    """Фикстура для сервиса задач"""
    from app.crud.task import TaskService
    return TaskService(db_session)


@pytest.fixture
def sample_task_data():
    """Фикстура с примером данных задачи"""
    return {
        "title": "Test Task",
        "description": "Test Description",
        "status": "created"
    }


@pytest.fixture
def created_task(client, sample_task_data):
    """Создает задачу и возвращает ее данные"""
    response = client.post("/tasks/", json=sample_task_data)
    return response.json()