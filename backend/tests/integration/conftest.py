
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from config import DATABASE_USER, DATABASE_PASSWORD
from database import Database, Base, ensure_database_exists, get_db
from main import app
from sheets.models import Sheet, Column, Cell

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

    _insert_model_instance_to_database(sheet, db_session)

    try:
        yield sheet
    finally:
        db_session.delete(sheet)


def _insert_model_instance_to_database(model_instance: Base, db_session: Session):
    db_session.add(model_instance)
    db_session.commit()
    db_session.refresh(model_instance)


@pytest.fixture(scope="module")
def int_column(db_session, sheet):
    column = Column(name="int_column", type="int", sheet=sheet)

    _insert_model_instance_to_database(column, db_session)

    try:
        yield column
    finally:
        db_session.delete(column)


@pytest.fixture(scope="module")
def int_cell(db_session, int_column):
    cell = Cell(row_index=1, value=0, column=int_column)

    _insert_model_instance_to_database(cell, db_session)

    try:
        yield cell
    finally:
        db_session.delete(cell)
