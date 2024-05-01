from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from database import get_db
from .exceptions import SheetCreationException
from .models import Sheet, Cell
from .schemas import CELL_NAME_KEY, CELL_TYPE_KEY
from .utils.cell_utils import parse_sheet_cells

router = APIRouter()


@router.post("/sheets/")
def create_sheet(sheet_data: Dict, db: Session = Depends(get_db)):
    try:
        created_sheet = Sheet()
        db.add(created_sheet)

        _add_cells_to_db(sheet_data, created_sheet, db)

        db.commit()

        return {
            "success": True,
            "created_id": created_sheet.id
        }
    except SheetCreationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while trying to insert sheet into database:\n{str(e)}"
        )


def _add_cells_to_db(sheet_data: Dict, created_sheet: Sheet, db: Session):
    for cell in parse_sheet_cells(sheet_data):
        db.add(
            Cell(
                name=cell[CELL_NAME_KEY],
                type=cell[CELL_TYPE_KEY],
                sheet=created_sheet
            )
        )
