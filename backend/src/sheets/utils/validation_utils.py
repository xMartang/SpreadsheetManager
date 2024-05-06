from sheets.consts import COLUMN_NAME_KEY, COLUMN_TYPE_KEY
from sheets.exceptions import InvalidSheetSchemaException, InvalidCellTypeException
from sheets.utils.column_type_converter import COLUMN_TYPE_VALUE_CONVERTER

REQUIRED_COLUMN_KEYS = [COLUMN_NAME_KEY, COLUMN_TYPE_KEY]


def is_cell_value_valid(cell_value: str, column_type: str) -> bool:
    if is_column_type_invalid(column_type):
        raise InvalidCellTypeException(
            f"Type `{column_type}` is invalid or unsupported...\n"
            f"Supported types: {COLUMN_TYPE_VALUE_CONVERTER.keys()}"
        )

    try:
        # If the conversion succeeds, then the value is valid
        COLUMN_TYPE_VALUE_CONVERTER[column_type](cell_value)

        return True
    except ValueError:
        return False


def ensure_sheet_column_valid(sheet_column: dict) -> None:
    if are_column_keys_invalid(sheet_column):
        raise InvalidSheetSchemaException(
            f"Column `{sheet_column}` is invalid...\n"
            f"Columns must contain the following keys: {REQUIRED_COLUMN_KEYS}"
        )

    if is_column_type_invalid(sheet_column[COLUMN_TYPE_KEY]):
        raise InvalidSheetSchemaException(
            f"Cell type `{sheet_column[COLUMN_TYPE_KEY]}` is invalid or unsupported...\n"
            f"Supported cell types: {COLUMN_TYPE_VALUE_CONVERTER.keys()}"
        )


def are_column_keys_invalid(sheet_column: dict) -> bool:
    """
    The cell is invalid if it doesn't contain any of the required keys
    """
    return not isinstance(sheet_column, dict) or any(
        required_key not in sheet_column for required_key in REQUIRED_COLUMN_KEYS)


def is_column_type_invalid(column_type: str) -> bool:
    return column_type.lower() not in COLUMN_TYPE_VALUE_CONVERTER
