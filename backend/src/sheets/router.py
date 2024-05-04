import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from sheets.consts import COLUMN_NAME_KEY, COLUMN_TYPE_KEY
from sheets.exceptions import SheetAPIException
from sheets.models import Sheet, Column
from sheets.schemas import CreateSheetRequest, SetCellValueRequest
from sheets.utils.database_utils import get_sheet_from_database_as_json, upsert_cell_value, \
    is_cell_value_lookup_function, get_value_of_lookup_cell, ensure_sheet_exists
from sheets.utils.parsing_utils import parse_sheet_columns
from sheets.utils.validation_utils import is_cell_value_valid

router = APIRouter()

CREATED_ID_KEY = "created_id"


@router.post("/sheets/", status_code=status.HTTP_201_CREATED)
async def create_sheet(create_sheet_request: CreateSheetRequest, db_session: Session = Depends(get_db)):
    try:
        logging.debug("Creating sheet...")
        created_sheet = Sheet()
        db_session.add(created_sheet)

        logging.debug("Adding all columns to the database...")
        await _add_columns_to_db(create_sheet_request.columns, created_sheet, db_session)

        db_session.commit()

        logging.info(f"Successfully created sheet with id {created_sheet.id}!")
        return {CREATED_ID_KEY: created_sheet.id}
    except SheetAPIException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def _add_columns_to_db(sheet_columns: list[dict], created_sheet: Sheet, db_session: Session) -> None:
    for column in parse_sheet_columns(sheet_columns):
        db_session.add(
            Column(
                name=column[COLUMN_NAME_KEY],
                type=column[COLUMN_TYPE_KEY],
                sheet=created_sheet
            )
        )


@router.get("/sheets/{sheet_id}/", status_code=status.HTTP_200_OK)
async def get_sheet_by_id(sheet_id: int, db_session: Session = Depends(get_db)):
    try:
        return get_sheet_from_database_as_json(sheet_id, db_session)
    except SheetAPIException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/sheets/{sheet_id}/set_cell_value", status_code=status.HTTP_200_OK)
async def set_cell_value(
        sheet_id: int, set_cell_value_request: SetCellValueRequest, db_session: Session = Depends(get_db)):
    ensure_sheet_exists(sheet_id, db_session)

    column_name, new_cell_value, row_index = \
        set_cell_value_request.column_name, set_cell_value_request.value, set_cell_value_request.row_index

    logging.debug(f"Getting the requested column '{column_name}' in sheet '{sheet_id}'...")
    column = db_session.scalar(
        select(Column).where(Column.sheet_id == sheet_id, Column.name == column_name))

    if not column:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Column with name '{column_name}' in sheet {sheet_id} doesn't exist."
        )

    _ensure_cell_value_is_valid(new_cell_value, row_index, column, db_session)

    inserted_cell = upsert_cell_value(db_session, column, row_index, new_cell_value)

    logging.info(f"Successfully inserted/updated cell with id {inserted_cell.id}!")
    return {CREATED_ID_KEY: inserted_cell.id}


def _ensure_cell_value_is_valid(cell_value, row_index, column, db_session):
    logging.debug(f"Ensuring that cell value '{cell_value}' in row {row_index} is valid...")

    try:
        if is_cell_value_lookup_function(cell_value):
            logging.debug(f"Finding the actual value of the lookup function '{cell_value}'...")
            cell_value = get_value_of_lookup_cell(cell_value, row_index, column, db_session)

        if not is_cell_value_valid(cell_value, column.type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Value '{cell_value}' doesn't match the column type (column type: '{column.type}')."
            )
    except SheetAPIException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
