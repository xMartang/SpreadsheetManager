import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from database import Base
from sheets.models import Sheet, Cell, Column


@pytest.fixture
def db_session_mock() -> UnifiedAlchemyMagicMock:
    session = UnifiedAlchemyMagicMock()

    yield session


@pytest.fixture
def sheet(db_session_mock) -> Sheet:
    sheet = Sheet(id=0)

    _insert_model_instance_to_database(sheet, db_session_mock)

    yield sheet


@pytest.fixture
def int_column(sheet, db_session_mock) -> Column:
    column = Column(id=0, name="int_column", type="int", sheet=sheet, sheet_id=sheet.id)

    _insert_model_instance_to_database(column, db_session_mock)

    yield column


@pytest.fixture
def int_cell(int_column, db_session_mock) -> Cell:
    cell = Cell(id=0, row_index=1, value="1", column=int_column, column_id=int_column.id)

    _insert_model_instance_to_database(cell, db_session_mock)

    yield cell


def _insert_model_instance_to_database(model_instance: Base, db_session: UnifiedAlchemyMagicMock):
    db_session.add(model_instance)
    db_session.commit()
    db_session.refresh(model_instance)
