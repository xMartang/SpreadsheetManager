import os

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from config import ALEMBIC_DATABASE_CONFIG_FILE_PATH
from database import Database, Base, get_db
from main import app
from sheets.models import Sheet, Column, Cell


@pytest.fixture(scope="session")
def http_client() -> TestClient:
    yield TestClient(app)


@pytest.fixture(scope="session")
def db_session() -> Session:
    _migrate_test_database_to_latest_revision()

    db = next(get_db())

    try:
        yield db
    finally:
        _clean_test_database()


def _migrate_test_database_to_latest_revision():
    alembic_config = Config(ALEMBIC_DATABASE_CONFIG_FILE_PATH)

    relative_script_location = alembic_config.get_main_option("script_location")

    alembic_config.set_main_option(
        "script_location",
        os.path.join(os.path.dirname(ALEMBIC_DATABASE_CONFIG_FILE_PATH), relative_script_location)
    )
    alembic_config.set_main_option("sqlalchemy.url", str(Database().engine.url))

    command.upgrade(alembic_config, "head")


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
