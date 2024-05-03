
import pytest

from sheets.models import Sheet, Cell


@pytest.fixture(scope="module")
def sheet():
    yield Sheet(id=0)


@pytest.fixture(scope="module")
def int_sheet_cell(sheet):
    yield Cell(name="int_sheet_cell", type="int", value=0, sheet_id=sheet.id)
