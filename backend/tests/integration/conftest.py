
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from config import DATABASE_USER, DATABASE_PASSWORD

from main import app
from database import Database, Base, ensure_database_exists, get_db

DATABASE_TEST_NAME = "test_spreadsheet"

Database.SQLALCHEMY_DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost/{DATABASE_TEST_NAME}'

# Create the test database if it doesn't exist
ensure_database_exists()


@pytest.fixture(scope="session")
def http_client() -> TestClient:
    yield TestClient(app)


@pytest.fixture(scope="session")
def db_session() -> Session:
    db = next(get_db())

    try:
        yield db
    finally:
        _clean_test_database()


def _clean_test_database():
    with Database().engine.connect() as connection:
        transaction = connection.begin()

        for tbl in reversed(Base.metadata.sorted_tables):
            connection.execute(tbl.delete())

        transaction.commit()
