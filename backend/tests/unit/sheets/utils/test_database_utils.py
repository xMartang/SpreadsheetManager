import pytest

from sheets.consts import COLUMN_NAME_KEY, COLUMN_TYPE_KEY, COLUMNS_KEY, CELLS_KEY
from sheets.exceptions import DatabaseObjectNotFoundException, InvalidCellValueException
from sheets.models import Cell
from sheets.utils.database_utils import LOOKUP_COLUMN_NAME_KEY, LOOKUP_ROW_INDEX_KEY, upsert_cell_value, \
    get_sheet_from_database_as_json, ensure_sheet_exists, _get_cells_from_column_as_json, _get_lookup_cell_value, \
    _is_circular_lookup_function, get_value_of_lookup_cell


def test_upsert_cell_value_to_new_cell(db_session_mock, int_column):
    row_index, cell_value = 1, "1"

    upsert_cell_value(db_session_mock, int_column, row_index, cell_value)

    inserted_cell = db_session_mock.query(Cell).filter_by(column_id=int_column.id, row_index=row_index).first()

    assert inserted_cell.value == cell_value


def test_upsert_cell_value_to_existing_cell(db_session_mock, int_column, int_cell):
    new_cell_value = int_cell.value + "1"

    upsert_cell_value(db_session_mock, int_column, int_cell.row_index, new_cell_value)

    updated_cell = db_session_mock.query(Cell).filter_by(column_id=int_column.id, row_index=int_cell.row_index).first()

    assert updated_cell.value == new_cell_value


def test_get_sheet_from_database_as_json_with_existing_sheet(db_session_mock, sheet, int_column, int_cell):
    sheet_json = get_sheet_from_database_as_json(sheet.id, db_session_mock)

    assert COLUMNS_KEY in sheet_json

    columns = sheet_json[COLUMNS_KEY]

    assert len(columns) == 1
    assert columns[0][COLUMN_NAME_KEY] == int_column.name and columns[0][COLUMN_TYPE_KEY] == int_column.type
    assert CELLS_KEY in columns[0]

    cells = columns[0][CELLS_KEY]

    assert len(cells) == 1 and cells[0] == int_cell.to_json()


def test_get_sheet_from_database_as_json_with_non_existing_sheet(db_session_mock):
    with pytest.raises(DatabaseObjectNotFoundException):
        get_sheet_from_database_as_json(-1, db_session_mock)


def test__get_cells_from_column_as_json_with_existing_column(db_session_mock, int_column, int_cell):
    cells_json = _get_cells_from_column_as_json(int_column, db_session_mock)

    assert len(cells_json) == 1


def test__get_cells_from_column_as_json_with_non_existing_column(db_session_mock, int_column):
    int_column.id = -1

    cells_json = _get_cells_from_column_as_json(int_column, db_session_mock)

    assert len(cells_json) == 0


def test_ensure_sheet_exists_with_existing_sheet(db_session_mock, sheet):
    ensure_sheet_exists(sheet.id, db_session_mock)


def test_ensure_sheet_exists_with_non_existing_sheet(db_session_mock):
    with pytest.raises(DatabaseObjectNotFoundException):
        ensure_sheet_exists(-1, db_session_mock)


def test__get_lookup_cell_value_with_existing_lookup_info(db_session_mock, int_column, int_cell):
    cell_value = _get_lookup_cell_value(
        {LOOKUP_COLUMN_NAME_KEY: int_column.name, LOOKUP_ROW_INDEX_KEY: int_cell.row_index},
        int_column.sheet_id,
        db_session_mock
    )

    assert cell_value == int_cell.value


def test__get_lookup_cell_value_with_non_existing_column(db_session_mock, sheet):
    with pytest.raises(DatabaseObjectNotFoundException):
        _get_lookup_cell_value(
            {LOOKUP_COLUMN_NAME_KEY: "non_existing_name", LOOKUP_ROW_INDEX_KEY: "1"},
            sheet.id,
            db_session_mock
        )


def test__get_lookup_cell_value_with_non_existing_row_index(db_session_mock, int_column):
    with pytest.raises(DatabaseObjectNotFoundException):
        _get_lookup_cell_value(
            {LOOKUP_COLUMN_NAME_KEY: int_column.name, LOOKUP_ROW_INDEX_KEY: "-1"},
            int_column.sheet_id,
            db_session_mock
        )


def test__is_circular_lookup_function_with_valid_lookup_info(db_session_mock, int_column, int_cell):
    assert not _is_circular_lookup_function(
        {LOOKUP_COLUMN_NAME_KEY: int_column.name + "A", LOOKUP_ROW_INDEX_KEY: int_cell.row_index},
        int_column,
        1
    )


def test__is_circular_lookup_function_with_circular_lookup_info(db_session_mock, int_column, int_cell):
    assert _is_circular_lookup_function(
        {LOOKUP_COLUMN_NAME_KEY: int_column.name, LOOKUP_ROW_INDEX_KEY: int_cell.row_index},
        int_column,
        int_cell.row_index
    )


def test_get_value_of_lookup_cell_with_valid_lookup_info(db_session_mock, int_column, int_cell):
    new_lookup_cell = Cell(
        id=int_cell.id + 1,
        row_index=int_cell.row_index + 1,
        value=f"lookup({int_column.name},{int_cell.row_index})",
        column=int_column
    )

    db_session_mock.add(new_lookup_cell)
    db_session_mock.commit()

    lookup_cell_value = get_value_of_lookup_cell(
        f"lookup({int_column.name},{new_lookup_cell.row_index})",
        new_lookup_cell.row_index + 1,
        int_column,
        db_session_mock
    )

    assert lookup_cell_value == int_cell.value


def test_get_value_of_lookup_cell_with_circular_lookup_info(db_session_mock, int_column, int_cell):
    new_lookup_cell = Cell(
        id=int_cell.id + 1,
        row_index=int_cell.row_index + 1,
        value=f"lookup({int_column.name},{int_cell.row_index})",
        column=int_column
    )

    db_session_mock.add(new_lookup_cell)
    db_session_mock.commit()

    with pytest.raises(InvalidCellValueException):
        get_value_of_lookup_cell(
            f"lookup({int_column.name},{int_cell.row_index})",
            int_cell.row_index,
            int_column,
            db_session_mock
        )


def test_get_value_of_lookup_cell_with_invalid_lookup_info(db_session_mock, int_column, int_cell):
    with pytest.raises(InvalidCellValueException):
        get_value_of_lookup_cell(
            f"lookup(invalid lookup parameters)",
            int_cell.row_index,
            int_column,
            db_session_mock
        )
