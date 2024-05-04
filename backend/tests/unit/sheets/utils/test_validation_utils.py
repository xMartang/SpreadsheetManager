
import pytest

from sheets.exceptions import InvalidCellTypeException
from sheets.consts import COLUMN_NAME_KEY, COLUMN_TYPE_KEY
from sheets.utils.validation_utils import is_cell_value_valid, is_column_type_invalid, are_column_keys_invalid


def test_is_cell_value_valid_method_with_unknown_type(db_session_mock):
    with pytest.raises(InvalidCellTypeException):
        is_cell_value_valid("", "unknown_type")


@pytest.mark.parametrize(
    'column_type, cell_value, expected_result', [
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
def test_is_cell_value_valid_method(column_type, cell_value, expected_result):
    assert is_cell_value_valid(cell_value, column_type) == expected_result


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
def test_is_column_type_invalid_method(cell_type, expected_result):
    assert is_column_type_invalid(cell_type) == expected_result


@pytest.mark.parametrize(
    'cell_data, expected_result',
    [({COLUMN_NAME_KEY: "", COLUMN_TYPE_KEY: ""}, False),  # Valid
     ({"naame": "", COLUMN_TYPE_KEY: ""}, True),  # Invalid, name typo
     ({COLUMN_NAME_KEY: "", "typo": ""}, True),  # Invalid, type typo
     ({COLUMN_NAME_KEY: ""}, True),  # Invalid, type missing
     ({COLUMN_TYPE_KEY: ""}, True),  # Invalid, name missing
     ("invalid_cell_data_type", True)]  # Invalid, not a dictionary
)
def test_are_column_keys_invalid_method(cell_data, expected_result):
    assert are_column_keys_invalid(cell_data) == expected_result
