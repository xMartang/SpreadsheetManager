import pytest

from sheets.utils.parsing_utils import parse_sheet_columns
from sheets.consts import COLUMN_NAME_KEY, COLUMN_TYPE_KEY
from sheets.exceptions import InvalidSheetSchemaException


@pytest.mark.parametrize(
    'sheet_columns, expected_parsed_cells_amount', [
        ([{COLUMN_NAME_KEY: "A", COLUMN_TYPE_KEY: "boolean"}], 1),
        ([{COLUMN_NAME_KEY: "A", COLUMN_TYPE_KEY: "int"}, {COLUMN_NAME_KEY: "B", COLUMN_TYPE_KEY: "string"}], 2),
        ([{COLUMN_NAME_KEY: "duplicate_name", COLUMN_TYPE_KEY: "double"},
          {COLUMN_NAME_KEY: "duplicate_name", COLUMN_TYPE_KEY: "boolean"}], 1),
        ([{COLUMN_NAME_KEY: "A", COLUMN_TYPE_KEY: "invalid_type"}, {COLUMN_NAME_KEY: "B", COLUMN_TYPE_KEY: "boolean"}], 0),
        ({}, 0)
    ]
)
def test_parse_sheet_columns_method(sheet_columns, expected_parsed_cells_amount):
    parsed_cells_amount = 0

    try:
        for _ in parse_sheet_columns(sheet_columns):
            parsed_cells_amount += 1
    except InvalidSheetSchemaException:
        assert parsed_cells_amount == expected_parsed_cells_amount
