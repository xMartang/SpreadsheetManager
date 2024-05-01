from sheets.exceptions import InvalidSheetSchemaException
from sheets.schemas import COLUMNS_DATA_KEY, REQUIRED_CELL_KEYS, CELL_TYPE_KEY, CELL_NAME_KEY


CELL_TYPE_VALUE_CONVERTER = {
    "boolean": bool,
    "int": int,
    "double": float,
    "string": str
}


def parse_sheet_cells(sheet_data: dict):
    parsed_sheet_cells = set()

    if COLUMNS_DATA_KEY not in sheet_data:
        raise InvalidSheetSchemaException(f"Sheet schema must contain `{COLUMNS_DATA_KEY}` key...")

    for sheet_cell in sheet_data[COLUMNS_DATA_KEY]:
        _ensure_sheet_cell_valid(sheet_cell)

        if sheet_cell[CELL_NAME_KEY] in parsed_sheet_cells:
            raise InvalidSheetSchemaException(f"A cell with the name '{sheet_cell[CELL_NAME_KEY]}' already exists...")

        # Add to parsed sheet cells to avoid name duplication
        parsed_sheet_cells.add(sheet_cell[CELL_NAME_KEY])

        yield sheet_cell


def _ensure_sheet_cell_valid(sheet_cell: dict):
    if _are_cell_keys_invalid(sheet_cell):
        raise InvalidSheetSchemaException(
            f"Cell `{sheet_cell}` is invalid...\n"
            f"Cells must contain the following keys: {REQUIRED_CELL_KEYS}"
        )

    if _is_cell_type_invalid(sheet_cell[CELL_TYPE_KEY]):
        raise InvalidSheetSchemaException(
            f"Cell type `{sheet_cell[CELL_TYPE_KEY]}` is invalid or unsupported...\n"
            f"Supported cell types: {CELL_TYPE_VALUE_CONVERTER.keys()}"
        )


def _are_cell_keys_invalid(sheet_cell: dict):
    """
    The cell is invalid if it doesn't contain any of the required keys
    """
    return not isinstance(sheet_cell, dict) or any(required_key not in sheet_cell for required_key in REQUIRED_CELL_KEYS)


def _is_cell_type_invalid(cell_type: str):
    return cell_type.lower() not in CELL_TYPE_VALUE_CONVERTER

