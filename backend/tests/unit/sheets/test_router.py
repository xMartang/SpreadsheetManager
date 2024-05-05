import pytest

from sheets.models import Column
from sheets.router import _add_columns_to_db

pytest_plugins = ('pytest_asyncio',)

VALID_COLUMNS = [
    {
        "name": "A",
        "type": "boolean"
    },
    {
        "name": "B",
        "type": "int"
    },
    {
        "name": "C",
        "type": "double"
    },
    {
        "name": "D",
        "type": "string"
    }
]


@pytest.mark.asyncio
async def test__add_columns_to_db(db_session_mock, sheet):
    await _add_columns_to_db(VALID_COLUMNS, sheet, db_session_mock)

    db_session_mock.commit()

    assert db_session_mock.query(Column).filter_by(sheet_id=sheet.id).count() == len(VALID_COLUMNS)
