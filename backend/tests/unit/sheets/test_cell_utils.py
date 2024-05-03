import pytest

from sheets.utils.cell_utils import CELL_NAME_KEY, CELL_TYPE_KEY, \
    is_cell_value_valid, parse_sheet_cells,  _is_cell_type_invalid, _are_cell_keys_invalid
from sheets.exceptions import InvalidSheetSchemaException, InvalidCellTypeException


def test_is_cell_value_valid_method_with_unknown_type():
    with pytest.raises(InvalidCellTypeException):
        is_cell_value_valid("", "unknown_type")


@pytest.mark.parametrize(
    'cell_type, cell_value, expected_result', [
        ("boolean", "True", True),
        ("boolean", "False", True),
        ("boolean", "invalid_boolean_value", False),
        ("string", "test", True),
        ("int", "53", True),
        ("int", "invalid_int_value", False),
        ("double", "1.337", True),
        ("double", "invalid_double_value", False)
    ]
)
def test_is_cell_value_valid_method(cell_type, cell_value, expected_result):
    assert is_cell_value_valid(cell_value, cell_type) == expected_result


@pytest.mark.parametrize(
    'sheet_columns, expected_parsed_cells_amount', [
        ([{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "boolean"}], 1),
        ([{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "int"}, {CELL_NAME_KEY: "B", CELL_TYPE_KEY: "string"}], 2),
        ([{CELL_NAME_KEY: "duplicate_name", CELL_TYPE_KEY: "double"},
          {CELL_NAME_KEY: "duplicate_name", CELL_TYPE_KEY: "boolean"}], 1),
        ([{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "invalid_type"}, {CELL_NAME_KEY: "B", CELL_TYPE_KEY: "boolean"}], 0),
        ({}, 0)
    ]
)
def test_parse_sheet_cells_method(sheet_columns, expected_parsed_cells_amount):
    parsed_cells_amount = 0

    try:
        for _ in parse_sheet_cells(sheet_columns):
            parsed_cells_amount += 1
    except InvalidSheetSchemaException:
        assert parsed_cells_amount == expected_parsed_cells_amount


@pytest.mark.parametrize(
    'cell_type, expected_result', [
        ("boolean", False),
        ("string", False),
        ("int", False),
        ("double", False),
        ("DoUbLe", False),
        ("unknown_type", True)
    ]
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
