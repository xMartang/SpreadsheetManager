from sheets.exceptions import InvalidSheetSchemaException
from sheets.schemas import COLUMNS_DATA_KEY, REQUIRED_CELL_KEYS, CELL_TYPE_KEY


CELL_TYPE_VALUE_CONVERTER = {
    "boolean": bool,
    "int": int,
    "double": float,
    "string": str
}


def parse_sheet_cells(sheet_data: dict):
    if COLUMNS_DATA_KEY not in sheet_data:
        raise InvalidSheetSchemaException("Sheet schema must contain `columns` key...")

    for sheet_cell in sheet_data[COLUMNS_DATA_KEY]:
        if _is_cell_invalid(sheet_cell):
            raise InvalidSheetSchemaException(
                f"Cell `{sheet_cell}` is invalid...\n"
                f"Cells must contain the following keys: {REQUIRED_CELL_KEYS}"
            )

        if _is_cell_type_invalid(sheet_cell):
            raise InvalidSheetSchemaException(
                f"Cell type `{sheet_cell[CELL_TYPE_KEY]}` is invalid or unsupported...\n"
                f"Supported cell types: {CELL_TYPE_VALUE_CONVERTER.keys()}"
            )

        yield sheet_cell


def _is_cell_invalid(sheet_cell):
    """
    The cell is invalid if it's not a json object (dict) or if it doesn't contain any of the required keys
    """
    return not isinstance(sheet_cell, dict) or any(required_key not in sheet_cell for required_key in REQUIRED_CELL_KEYS)


def _is_cell_type_invalid(sheet_cell):
    return sheet_cell[CELL_TYPE_KEY] not in CELL_TYPE_VALUE_CONVERTER

