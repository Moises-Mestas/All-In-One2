import pytest
import packages.core.database as db


def test_database_config():
    assert db.DATABASE_URL is not None
    assert "postgresql" in db.DATABASE_URL


def test_engine_exists():
    assert db.engine is not None


def test_async_session_maker():
    assert db.async_session_maker is not None


def test_get_db_is_generator():
    import inspect
    assert inspect.isasyncgenfunction(db.get_db)