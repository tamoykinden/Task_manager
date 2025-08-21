from fastapi import FastAPI
from app.api.api import router
from app.database import engine, Base


app = FastAPI(
    title="Task Manager API",
    description="""
    API для управления задачами
    
    Возможности:
    -  Создание задач
    - Получение списка задач
    - Получение задачи по ID  
    - Обновление задач
    - Удаление задач
    
    Статусы задач:
    - created - создана
    - in_progress - в работе
    - completed - завершена
    """,
    version="1.0.0",
    contact={
        "name": "Ваше имя",
        "email": "ваш.email@example.com",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(router, prefix='/tasks')

Base.metadata.create_all(bind=engine)

@app.get('/')
def read_root():
    return {'message': 'Task manager is running'}

@app.get('/health')
def health_check():
    return {'status': 'OK'}