
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import insert
from sqlalchemy.orm import Session

from config import DATABASE_USER, DATABASE_PASSWORD
from database import Database, Base, ensure_database_exists, get_db
from main import app
from sheets.models import Sheet, Cell

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


@pytest.fixture(scope="module")
def sheet(db_session):
    sheet = Sheet()

    # Insert sheet to the database
    db_session.add(sheet)
    db_session.commit()

    try:
        yield sheet
    finally:
        db_session.delete(sheet)


@pytest.fixture(scope="module")
def int_sheet_cell(db_session, sheet):
    cell = Cell(name="int_sheet_cell", type="int", value=0, sheet_id=sheet.id)

    # Insert cell to the database
    db_session.add(cell)
    db_session.commit()

    try:
        yield cell
    finally:
        db_session.delete(cell)
