from fastapi import FastAPI
from app.api.api import router
from app.database import engine, Base


"""Инициилизирую приложение Fastapi"""
app = FastAPI(title='Task Manager API', description='API для управления задачами', version='1.0.0')

app.include_router(router, prefix='/tasks')

@app.on_event('startup')
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get('/')
def read_root():
    return {'message': 'Task manager is running'}

@app.get('/health')
def health_check():
    return {'status': 'OK'}