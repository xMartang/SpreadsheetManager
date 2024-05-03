from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from database import get_db
from .exceptions import SheetCreationException
from .models import Sheet, Cell
from .schemas import CreateSheetRequest, SetCellValueRequest
from .utils.cell_utils import CELL_NAME_KEY, CELL_TYPE_KEY, parse_sheet_cells, is_cell_value_valid

router = APIRouter()

CREATED_ID_KEY = "created_id"


@router.post("/sheets/")
async def create_sheet(create_sheet_request: CreateSheetRequest, db_session: Session = Depends(get_db)):
    try:
        created_sheet = Sheet()
        db_session.add(created_sheet)

        await _add_cells_to_db(create_sheet_request.columns, created_sheet, db_session)

        db_session.commit()

        return {
            "success": True,
            CREATED_ID_KEY: created_sheet.id
        }
    except SheetCreationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while trying to insert sheet into database:\n{str(e)}"
        )


async def _add_cells_to_db(sheet_columns: list, created_sheet: Sheet, db_session: Session):
    for cell in parse_sheet_cells(sheet_columns):
        db_session.add(
            Cell(
                name=cell[CELL_NAME_KEY],
                type=cell[CELL_TYPE_KEY],
                sheet=created_sheet
            )
        )


@router.post("/sheets/{sheet_id}/set_cell_value")
async def set_cell_value(sheet_id: int, set_cell_value_request: SetCellValueRequest, db_session: Session = Depends(get_db)):
    cell_name, new_cell_value = set_cell_value_request.name, set_cell_value_request.value

    try:
        # Get the value type of the cell we need to set the value of
        cell_type = db_session.scalar(
            select(Cell.type).where(Cell.sheet_id == sheet_id, Cell.name == cell_name)
        )

        if not cell_type:
            raise HTTPException(
                status_code=400, detail=f"Cell with name '{cell_name}' in sheet {sheet_id} doesn't exist.")

        if not is_cell_value_valid(new_cell_value, cell_type):
            raise HTTPException(
                status_code=400,
                detail=f"Given value '{new_cell_value}' isn't valid (value must be of type '{cell_type}')."
            )

        db_session.execute(
            update(Cell)
            .where(Cell.sheet_id == sheet_id, Cell.name == cell_name)
            .values(value=new_cell_value)
        )

        db_session.commit()

        return {
            "success": True
        }
    except DatabaseError as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while trying to insert sheet into database:\n{str(e)}"
        )

