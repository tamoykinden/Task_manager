from app.config import DSN, TEST_DSN

def test_config_values():
    assert DSN is not None
    assert TEST_DSN is not None