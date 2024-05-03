import pdb

import pytest

from sheets.models import Sheet, Cell
from sheets.router import CREATED_ID_KEY
from sheets.utils.cell_utils import CELL_NAME_KEY, CELL_TYPE_KEY, CELL_VALUE_KEY

COLUMNS_KEY = "columns"


@pytest.mark.parametrize(
    'sheet_data', [
        {COLUMNS_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "boolean"}]},
        {COLUMNS_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "DOUBLE"}]},
        {COLUMNS_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "int"}, {CELL_NAME_KEY: "B", CELL_TYPE_KEY: "string"}]},
    ]
)
def test_create_sheet_endpoint_with_valid_sheet_data_schema(http_client, db_session, sheet_data):
    response = http_client.post("/sheets/", json=sheet_data,)

    assert response.status_code == 200

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

    assert response.status_code >= 400

    response_data = response.json()

    assert CREATED_ID_KEY not in response_data


def test_set_cell_value_endpoint_with_valid_data_schema(http_client, db_session, int_sheet_cell):
    set_cell_value_data = {CELL_NAME_KEY: int_sheet_cell.name, CELL_VALUE_KEY: "123"}

    response = http_client.post(f"/sheets/{int_sheet_cell.sheet_id}/set_cell_value", json=set_cell_value_data)

    assert response.status_code == 200

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
def test_set_cell_value_endpoint_with_invalid_sheet_data_schema(http_client, int_sheet_cell, set_cell_value_json):
    response = http_client.post(f"/sheets/{int_sheet_cell.sheet_id}/set_cell_value", json=set_cell_value_json)

    assert response.status_code >= 400
