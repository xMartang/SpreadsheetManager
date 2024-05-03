import pytest
from fastapi import status
from sqlalchemy import select, desc

from sheets.models import Sheet
from sheets.router import CREATED_ID_KEY
from sheets.utils.cell_utils import CELL_NAME_KEY, CELL_TYPE_KEY, CELL_VALUE_KEY, COLUMNS_KEY


@pytest.mark.parametrize(
    'sheet_data', [
        {COLUMNS_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "boolean"}]},
        {COLUMNS_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "DOUBLE"}]},
        {COLUMNS_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "int"}, {CELL_NAME_KEY: "B", CELL_TYPE_KEY: "string"}]},
    ]
)
def test_create_sheet_endpoint_with_valid_sheet_data_schema(http_client, db_session, sheet_data):
    response = http_client.post("/sheets/", json=sheet_data,)

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
        {COLUMNS_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "invalid"}]},
        {COLUMNS_KEY: [{CELL_NAME_KEY: "duplicate_name", CELL_TYPE_KEY: "double"},
                       {CELL_NAME_KEY: "duplicate_name", CELL_TYPE_KEY: "boolean"}]}
    ]
)
def test_create_sheet_endpoint_with_invalid_sheet_data_schema(http_client, sheet_data):
    response = http_client.post("/sheets/", json=sheet_data)

    assert response.status_code >= status.HTTP_400_BAD_REQUEST

    response_data = response.json()

    assert CREATED_ID_KEY not in response_data


def test_set_cell_value_endpoint_with_valid_data_schema(http_client, db_session, int_sheet_cell):
    set_cell_value_data = {CELL_NAME_KEY: int_sheet_cell.name, CELL_VALUE_KEY: "123"}

    response = http_client.post(f"/sheets/{int_sheet_cell.sheet_id}/set_cell_value", json=set_cell_value_data)

    assert response.status_code == status.HTTP_200_OK

    db_session.refresh(int_sheet_cell)

    assert int_sheet_cell.value == set_cell_value_data[CELL_VALUE_KEY]


@pytest.mark.parametrize(
    'set_cell_value_json', [
        {},
        {"naame": "", CELL_VALUE_KEY: "a"},
        {CELL_NAME_KEY: "", "vaalue": " a"},
        "invalid_json_argument",
        {CELL_NAME_KEY: "non_existing_cell_name", CELL_VALUE_KEY: ""},
        {CELL_NAME_KEY: "int_sheet_cell", CELL_VALUE_KEY: "invalid_int_value"},
    ]
)
def test_set_cell_value_endpoint_with_invalid_sheet_data_schema(
        set_cell_value_json, http_client, int_sheet_cell, db_session):
    current_value = int_sheet_cell.value

    response = http_client.post(f"/sheets/{int_sheet_cell.sheet_id}/set_cell_value", json=set_cell_value_json)

    assert response.status_code >= status.HTTP_400_BAD_REQUEST

    db_session.refresh(int_sheet_cell)

    assert int_sheet_cell.value == current_value


def test_get_sheet_by_id_with_existing_sheet(http_client, sheet, int_sheet_cell):
    response = http_client.get(f"/sheets/{sheet.id}")

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert COLUMNS_KEY in response_data
    assert len(response_data[COLUMNS_KEY]) == 1
    assert response_data[COLUMNS_KEY][0] == int_sheet_cell.to_json()


def test_get_sheet_by_id_with_non_existing_sheet(http_client, db_session):
    last_sheet_id = db_session.scalar(select(Sheet.id).order_by(desc(Sheet.id))) or 0

    response = http_client.get(f"/sheets/{last_sheet_id + 1}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = response.json()

    assert COLUMNS_KEY not in response_data
