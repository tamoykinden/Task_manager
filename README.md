# Task Manager API
FastAPI приложение для управления задачами с CRUD операциями.

## Функциональность
1. Создание, чтение, обновление, удаление задач
2. Статусы задач: created, in_progress, completed
3. Пагинация списка задач
4. Валидация входных данных
5. Автоматическая документация API

## Технологии
1. FastAPI
2. SQLAlchemy
3. PostgreSQL / SQLite
4. Pydantic
5. Pytest
6. Docker

## Установка и запуск
### Локальная разработка
Установите зависимости: pip install -r requirements.txt
Запустите приложение: uvicorn main:app --reload
Приложение будет доступно по адресу: http://localhost:8000

### Docker запуск
Запустите приложение с Docker Compose: docker-compose up --build
Приложение будет доступно по адресу: http://localhost:8000

## API Endpoints
### Tasks
GET /tasks - Получить список задач с пагинацией
POST /tasks - Создать новую задачу
GET /tasks/{task_id} - Получить задачу по ID
PATCH /tasks/{task_id} - Обновить задачу
DELETE /tasks/{task_id} - Удалить задачу

### System
GET / - Информация о приложении
GET /health - Проверка здоровья приложения
GET /docs - Интерактивная документация API
GET /redoc - Альтернативная документация

## Примеры запросов
### Создание задачи

curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Тестовая задача", "description": "Описание задачи"}'

### Получение списка задач

curl "http://localhost:8000/tasks/?skip=0&limit=10"

### Обновление задачи

curl -X PATCH "http://localhost:8000/tasks/{task_id}" \
     -H "Content-Type: application/json" \
     -d '{"status": "in_progress"}'

### Тестирование
Запуск всех тестов
pytest

### Запуск с покрытием кода
pytest --cov=app

Тестирование в Docker
docker-compose exec app pytest

### Переменные окружения
DSN - DSN для подключения к PostgreSQL

TEST_DSN - DSN для тестовой базы данных

DB_USER - пользователь PostgreSQL

DB_PASSWORD - пароль PostgreSQL

DB_NAME - имя базы данных

Документация
Swagger UI: http://localhost:8000/docs

## Docker команды

### Сборка и запуск
docker-compose up --build

### Запуск в фоновом режиме
docker-compose up -d

### Просмотр логов
docker-compose logs -f

### Остановка
docker-compose down

### Остановка с удалением volumes
docker-compose down -v

### Пересборка
docker-compose build

### Запуск команд в контейнере
docker-compose exec app bash
Разработка
Приложение использует автоматическую перезагрузку при изменении кода. Для разработки рекомендуется запускать с флагом --reload.

База данных автоматически создается при первом запуске. Миграции не требуются - SQLAlchemy автоматически создает таблицы.