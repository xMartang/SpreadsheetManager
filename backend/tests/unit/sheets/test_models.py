
from sheets.utils.cell_utils import CELL_NAME_KEY, CELL_TYPE_KEY, CELL_VALUE_KEY


def test_cell_to_json_method(int_sheet_cell):
    json_data = int_sheet_cell.to_json()

    assert CELL_NAME_KEY in json_data
    assert CELL_TYPE_KEY in json_data
    assert CELL_VALUE_KEY in json_data
