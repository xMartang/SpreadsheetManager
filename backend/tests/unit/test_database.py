import pytest

from database import get_db


def test_get_db():
    try:
        db = next(get_db())

        db.connection()
    except Exception as e:
        pytest.fail(f"An error occurred while trying to connect to the database: {e}")
