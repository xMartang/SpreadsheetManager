from typing import Generator

from sheets.exceptions import InvalidSheetSchemaException
from sheets.utils.validation_utils import COLUMN_NAME_KEY, ensure_sheet_column_valid


def parse_sheet_columns(sheet_columns: list[dict]) -> Generator[dict, dict, dict]:
    parsed_sheet_columns = set()

    for sheet_column in sheet_columns:
        ensure_sheet_column_valid(sheet_column)

        if sheet_column[COLUMN_NAME_KEY] in parsed_sheet_columns:
            raise InvalidSheetSchemaException(
                f"A column with the name '{sheet_column[COLUMN_NAME_KEY]}' already exists...")

        # Add to parsed sheet columns to avoid name duplication
        parsed_sheet_columns.add(sheet_column[COLUMN_NAME_KEY])

        yield sheet_column
