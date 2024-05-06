import logging
import re

from sqlalchemy.orm import Session

from sheets.consts import CELLS_KEY, LOOKUP_FUNCTION_NAME_PREFIX
from sheets.exceptions import InvalidCellValueException, DatabaseObjectNotFoundException
from sheets.models import Sheet, Cell, Column
from sheets.schemas import COLUMNS_KEY

from sheets.utils.column_type_converter import COLUMN_TYPE_VALUE_CONVERTER

LOOKUP_COLUMN_NAME_KEY = "column_name"
LOOKUP_ROW_INDEX_KEY = "row_index"

LOOKUP_CELL_VALUE_REGEX_PATTERN = re.compile(
    r"{LOOKUP_FUNCTION_NAME_PREFIX}\((?P<{column_name}>.*),(?P<{row_index}>\d*)\)".format(
        LOOKUP_FUNCTION_NAME_PREFIX=LOOKUP_FUNCTION_NAME_PREFIX,
        column_name=LOOKUP_COLUMN_NAME_KEY,
        row_index=LOOKUP_ROW_INDEX_KEY
    )
)


def get_value_of_lookup_cell(
        lookup_cell_value: str, original_row_index: int, original_column: Column, db_session: Session) -> str:
    lookup_info = LOOKUP_CELL_VALUE_REGEX_PATTERN.match(lookup_cell_value)

    if lookup_info is None:
        raise InvalidCellValueException(f"Value '{lookup_cell_value}' is not a valid lookup function value...")

    lookup_info = lookup_info.groupdict()
    logging.debug(f"Fetching the value of lookup function '{lookup_cell_value}'...")

    if _is_circular_lookup_function(lookup_info, original_column, original_row_index):
        raise InvalidCellValueException(f"The lookup function resulted in a circular reference, which is not allowed.")

    new_lookup_cell_value = _get_lookup_cell_value(lookup_info, original_column.sheet_id, db_session)

    if not is_cell_value_lookup_function(new_lookup_cell_value):
        logging.debug(f"Found the actual value {new_lookup_cell_value} of lookup function '{lookup_cell_value}'...")
        return new_lookup_cell_value

    return get_value_of_lookup_cell(new_lookup_cell_value, original_row_index, original_column, db_session)


def is_cell_value_lookup_function(cell_value):
    return LOOKUP_FUNCTION_NAME_PREFIX in str(cell_value)


def _is_circular_lookup_function(lookup_info: dict, original_column: Column, original_row_index: int):
    return lookup_info[LOOKUP_COLUMN_NAME_KEY] == original_column.name and \
        int(lookup_info[LOOKUP_ROW_INDEX_KEY]) == original_row_index


def _get_lookup_cell_value(lookup_info: dict, sheet_id: int, db_session: Session) -> str:
    column_name = lookup_info[LOOKUP_COLUMN_NAME_KEY]
    column = db_session.query(Column).filter_by(sheet_id=sheet_id, name=column_name).first()

    if column is None:
        raise DatabaseObjectNotFoundException(f"Column '{column_name}' wasn't found...")

    lookup_column_id = column.id
    row_index = int(lookup_info[LOOKUP_ROW_INDEX_KEY])
    lookup_cell = db_session.query(Cell).filter_by(column_id=lookup_column_id, row_index=row_index).first()

    if lookup_cell is None:
        raise DatabaseObjectNotFoundException(f"Cell in row '{row_index}' wasn't found...")

    return lookup_cell.value


def upsert_cell_value(db_session: Session, column: Column, row_index: int, new_cell_value: str) -> Cell:
    inserted_cell = db_session.query(Cell).filter_by(column_id=column.id, row_index=row_index).first()

    if not inserted_cell:
        logging.debug(f"Creating new cell in column {column.id}, row {row_index} with value {new_cell_value}...")
        inserted_cell = Cell(row_index=row_index, value=new_cell_value, column_id=column.id, column=column)
    else:
        logging.debug(f"Updating existing  cell in column {column.id}, row {row_index} with value {new_cell_value}...")
        inserted_cell.value = new_cell_value

    db_session.add(inserted_cell)
    db_session.commit()
    db_session.refresh(inserted_cell)

    return inserted_cell


def get_sheet_from_database_as_json(sheet_id: int, db_session: Session) -> dict:
    ensure_sheet_exists(sheet_id, db_session)

    sheet_data = {COLUMNS_KEY: []}
    columns = db_session.query(Column).filter_by(sheet_id=sheet_id).order_by(Column.id.asc()).all()

    logging.debug(f"Parsing all columns in sheet {sheet_id}...")

    for column in columns:
        current_column_json = column.to_json()
        current_column_json[CELLS_KEY] = _get_cells_from_column_as_json(column, db_session)

        sheet_data[COLUMNS_KEY].append(current_column_json)

    logging.info(f"Successfully parsed columns in sheet {sheet_id} to json format!")

    return sheet_data


def _get_cells_from_column_as_json(column: Column, db_session: Session) -> list[dict]:
    cells_json_data = []
    cells = db_session.query(Cell).filter_by(column_id=column.id).order_by(Cell.row_index.asc()).all()

    for cell in cells:
        if is_cell_value_lookup_function(cell.value):
            cell.value = get_value_of_lookup_cell(cell.value, cell.row_index, column, db_session)

        cell.value = COLUMN_TYPE_VALUE_CONVERTER[column.type](cell.value)

        cells_json_data.append(cell.to_json())

    return cells_json_data


def ensure_sheet_exists(sheet_id: int, db_session: Session) -> None:
    logging.debug(f"Ensuring that sheet with id {sheet_id} exists...")

    sheet = db_session.query(Sheet).filter_by(id=sheet_id).first()

    if not sheet:
        raise DatabaseObjectNotFoundException(f"Sheet with id {sheet_id} doesn't exist...")
