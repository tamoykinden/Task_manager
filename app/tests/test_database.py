def test_get_db(db_session):
    """Тест получения сессии БД"""
    from app.database import get_db
    db = next(get_db())
    assert db is not None
    db.close()