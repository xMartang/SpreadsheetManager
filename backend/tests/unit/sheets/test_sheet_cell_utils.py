import pytest

from sheets.schemas import CELL_NAME_KEY, CELL_TYPE_KEY, COLUMNS_DATA_KEY
from sheets.utils.sheet_cell_utils import _is_cell_type_invalid, _are_cell_keys_invalid, parse_sheet_cells
from sheets.exceptions import InvalidSheetSchemaException


@pytest.mark.parametrize(
    'cell_type, expected_result',
    [("boolean", False),
     ("string", False),
     ("int", False),
     ("double", False),
     ("DoUbLe", False),
     ("unknown_type", True)]
)
def test_is_cell_type_invalid_method(cell_type, expected_result):
    assert _is_cell_type_invalid(cell_type) == expected_result


@pytest.mark.parametrize(
    'cell_data, expected_result',
    [({CELL_NAME_KEY: "", CELL_TYPE_KEY: ""}, False),  # Valid
     ({"naame": "", CELL_TYPE_KEY: ""}, True),  # Invalid, name typo
     ({CELL_NAME_KEY: "", "typo": ""}, True),  # Invalid, type typo
     ({CELL_NAME_KEY: ""}, True),  # Invalid, type missing
     ({CELL_TYPE_KEY: ""}, True),  # Invalid, name missing
     ("invalid_cell_data_type", True)]  # Invalid, not a dictionary
)
def test_are_cell_keys_invalid_method(cell_data, expected_result):
    assert _are_cell_keys_invalid(cell_data) == expected_result


@pytest.mark.parametrize(
    'sheet_data, expected_parsed_cells_amount',
    [({COLUMNS_DATA_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "boolean"}]}, 1),

     ({COLUMNS_DATA_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "int"},
                          {CELL_NAME_KEY: "B", CELL_TYPE_KEY: "string"}]}, 2),

     ({COLUMNS_DATA_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "double"},
                          {CELL_NAME_KEY: "A", CELL_TYPE_KEY: "boolean"}]}, 1),  # Test Duplicate names

     ({COLUMNS_DATA_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "invalid"},
                          {CELL_NAME_KEY: "B", CELL_TYPE_KEY: "boolean"}]}, 0),  # Test Invalid type

     ({"cols": [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "invalid"},
                {CELL_NAME_KEY: "B", CELL_TYPE_KEY: "boolean"}]}, 0),  # Test Columns key

     ({}, 0)]  # Invalid, empty dictionary
)
def test_parse_sheet_cells_method(sheet_data, expected_parsed_cells_amount):
    parsed_cells_amount = 0

    try:
        for _ in parse_sheet_cells(sheet_data):
            parsed_cells_amount += 1
    except InvalidSheetSchemaException:
        assert parsed_cells_amount == expected_parsed_cells_amount


