from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, asc
from sqlalchemy.orm import Session

from database import get_db
from .exceptions import SheetCreationException
from .models import Sheet, Cell
from .schemas import CreateSheetRequest, SetCellValueRequest
from .utils.cell_utils import CELL_NAME_KEY, CELL_TYPE_KEY, COLUMNS_KEY, parse_sheet_cells, is_cell_value_valid

router = APIRouter()

CREATED_ID_KEY = "created_id"


@router.post("/sheets/", status_code=status.HTTP_201_CREATED)
async def create_sheet(create_sheet_request: CreateSheetRequest, db_session: Session = Depends(get_db)):
    try:
        created_sheet = Sheet()
        db_session.add(created_sheet)

        await _add_cells_to_db(create_sheet_request.columns, created_sheet, db_session)

        db_session.commit()

        return {CREATED_ID_KEY: created_sheet.id}
    except SheetCreationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def _add_cells_to_db(sheet_columns: list, created_sheet: Sheet, db_session: Session):
    for cell in parse_sheet_cells(sheet_columns):
        db_session.add(
            Cell(
                name=cell[CELL_NAME_KEY],
                type=cell[CELL_TYPE_KEY],
                sheet=created_sheet
            )
        )


@router.get("/sheets/{sheet_id}/", status_code=status.HTTP_200_OK)
async def get_sheet_by_id(sheet_id: int, db_session: Session = Depends(get_db)):
    sheet = db_session.scalar(select(Sheet).where(Sheet.id == sheet_id))

    if not sheet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sheet with id {sheet_id} doesn't exist..."
        )

    cells = db_session.scalars(select(Cell).where(Cell.sheet_id == sheet_id).order_by(asc(Cell.id)))

    return {COLUMNS_KEY: [cell.to_json() for cell in cells]}


@router.post("/sheets/{sheet_id}/set_cell_value", status_code=status.HTTP_200_OK)
async def set_cell_value(
        sheet_id: int, set_cell_value_request: SetCellValueRequest, db_session: Session = Depends(get_db)):
    cell_name, new_cell_value = set_cell_value_request.name, set_cell_value_request.value

    # Get the value type of the cell we need to set the value of
    cell_type = db_session.scalar(
        select(Cell.type).where(Cell.sheet_id == sheet_id, Cell.name == cell_name))

    if not cell_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cell with name '{cell_name}' in sheet {sheet_id} doesn't exist."
        )

    if not is_cell_value_valid(new_cell_value, cell_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Given value '{new_cell_value}' isn't valid (value must be of type '{cell_type}')."
        )

    db_session.execute(
        update(Cell)
        .where(Cell.sheet_id == sheet_id, Cell.name == cell_name)
        .values(value=new_cell_value)
    )

    db_session.commit()

    return {"success": True}
