import pytest
from fastapi import status
from sqlalchemy import select, desc

from sheets.consts import COLUMN_TYPE_KEY, COLUMN_NAME_KEY, COLUMNS_KEY, CELLS_KEY
from sheets.models import Sheet, Cell
from sheets.router import CREATED_ID_KEY

SET_CELL_COLUMN_NAME_KEY = "column_name"
SET_CELL_ROW_INDEX_KEY = "row_index"
SET_CELL_VALUE_KEY = "value"


@pytest.mark.parametrize(
    'sheet_data', [
        {COLUMNS_KEY: [{COLUMN_NAME_KEY: "A", COLUMN_TYPE_KEY: "boolean"}]},
        {COLUMNS_KEY: [{COLUMN_NAME_KEY: "A", COLUMN_TYPE_KEY: "DOUBLE"}]},
        {COLUMNS_KEY: [{COLUMN_NAME_KEY: "A", COLUMN_TYPE_KEY: "int"},
                       {COLUMN_NAME_KEY: "B", COLUMN_TYPE_KEY: "string"}]},
    ]
)
def test_create_sheet_endpoint_with_valid_sheet_data_schema(http_client, db_session, sheet_data):
    response = http_client.post("/sheets/", json=sheet_data, )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    assert CREATED_ID_KEY in response_data

    fetched_sheet = db_session.get(Sheet, response_data[CREATED_ID_KEY])

    assert fetched_sheet is not None


@pytest.mark.parametrize(
    'sheet_data', [
        {"cols": []},
        {},
        "invalid_json_argument",
        {COLUMNS_KEY: [{COLUMN_NAME_KEY: "A", COLUMN_TYPE_KEY: "invalid"}]},
        {COLUMNS_KEY: [{COLUMN_NAME_KEY: "duplicate_name", COLUMN_TYPE_KEY: "double"},
                       {COLUMN_NAME_KEY: "duplicate_name", COLUMN_TYPE_KEY: "boolean"}]}
    ]
)
def test_create_sheet_endpoint_with_invalid_sheet_data_schema(http_client, sheet_data):
    response = http_client.post("/sheets/", json=sheet_data)

    assert response.status_code >= status.HTTP_400_BAD_REQUEST

    response_data = response.json()

    assert CREATED_ID_KEY not in response_data


def test_set_cell_value_endpoint_with_valid_data_schema(http_client, db_session, int_column, int_cell):
    set_cell_value_data = {
        SET_CELL_COLUMN_NAME_KEY: int_column.name,
        SET_CELL_ROW_INDEX_KEY: int_cell.row_index,
        SET_CELL_VALUE_KEY: str(int(int_cell.value) + 1)
    }

    response = http_client.post(f"/sheets/{int_column.sheet_id}/set_cell_value", json=set_cell_value_data)

    assert response.status_code == status.HTTP_200_OK

    db_session.refresh(int_cell)

    assert int_cell.value == set_cell_value_data[SET_CELL_VALUE_KEY]


@pytest.mark.parametrize(
    'set_cell_value_json', [
        {},
        {"naame": "", SET_CELL_ROW_INDEX_KEY: 1, SET_CELL_VALUE_KEY: "a"},
        {SET_CELL_COLUMN_NAME_KEY: "", SET_CELL_ROW_INDEX_KEY: 1,  "vaalue": " a"},
        "invalid_json_argument",
        {SET_CELL_COLUMN_NAME_KEY: "non_existing_column_name", SET_CELL_ROW_INDEX_KEY: 1, SET_CELL_VALUE_KEY: ""},
        {SET_CELL_COLUMN_NAME_KEY: "int_cell", SET_CELL_ROW_INDEX_KEY: 1, SET_CELL_VALUE_KEY: "invalid_value"},
        {SET_CELL_COLUMN_NAME_KEY: "int_cell", SET_CELL_ROW_INDEX_KEY: 2, SET_CELL_VALUE_KEY: "lookup(invalid params)"},
    ]
)
def test_set_cell_value_endpoint_with_invalid_sheet_data_schema(
        set_cell_value_json, http_client, int_column, int_cell, db_session):
    current_value = int_cell.value

    if isinstance(set_cell_value_json, dict):
        set_cell_value_json[SET_CELL_ROW_INDEX_KEY] = int_cell.row_index

    response = http_client.post(f"/sheets/{int_column.sheet_id}/set_cell_value", json=set_cell_value_json)

    assert response.status_code >= status.HTTP_400_BAD_REQUEST

    db_session.refresh(int_cell)

    assert int_cell.value == current_value


def test_set_cell_value_endpoint_with_valid_lookup_value(http_client, int_column, int_cell, db_session):
    response = http_client.post(
        f"/sheets/{int_column.sheet_id}/set_cell_value",
        json={
            SET_CELL_COLUMN_NAME_KEY: int_column.name,
            SET_CELL_ROW_INDEX_KEY: int_cell.row_index + 1,
            SET_CELL_VALUE_KEY: f"lookup({int_column.name},{int_cell.row_index})"
        }
    )

    json_data = response.json()

    assert response.status_code >= status.HTTP_200_OK
    assert CREATED_ID_KEY in json_data

    inserted_cell = db_session.query(Cell).filter_by(id=json_data[CREATED_ID_KEY]).first()

    assert inserted_cell is not None


def test_set_cell_value_endpoint_with_circular_lookup_reference(http_client, int_column, int_cell, db_session):
    response = http_client.post(
        f"/sheets/{int_column.sheet_id}/set_cell_value",
        json={
            SET_CELL_COLUMN_NAME_KEY: int_column.name,
            SET_CELL_ROW_INDEX_KEY: int_cell.row_index,
            SET_CELL_VALUE_KEY: f"lookup({int_column.name},{int_cell.row_index})"
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_sheet_by_id_with_existing_sheet(http_client, int_column, int_cell):
    response = http_client.get(f"/sheets/{int_column.sheet_id}")

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert COLUMNS_KEY in response_data

    columns = response_data[COLUMNS_KEY]

    assert len(columns) == 1
    assert columns[0][COLUMN_NAME_KEY] == int_column.name
    assert CELLS_KEY in columns[0]

    cells = columns[0][CELLS_KEY]

    assert len(cells) == len(int_column.cells) and cells[0] == int_cell.to_json()


def test_get_sheet_by_id_with_non_existing_sheet(http_client, db_session):
    last_sheet_id = db_session.scalar(select(Sheet.id).order_by(desc(Sheet.id))) or 0

    response = http_client.get(f"/sheets/{last_sheet_id + 1}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = response.json()

    assert COLUMNS_KEY not in response_data
