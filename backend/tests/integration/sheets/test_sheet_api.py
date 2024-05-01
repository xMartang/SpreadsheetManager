
import pytest

from sheets.models import Sheet
from sheets.schemas import CELL_NAME_KEY, CELL_TYPE_KEY, COLUMNS_DATA_KEY
from sheets.router import CREATED_ID_KEY


@pytest.mark.parametrize(
    'sheet_data',
    [{COLUMNS_DATA_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "boolean"}]},
     {COLUMNS_DATA_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "int"}, {CELL_NAME_KEY: "B", CELL_TYPE_KEY: "string"}]},]
)
def test_create_valid_sheet_endpoint(http_client, db_session, sheet_data):
    response = _create_sheet_using_endpoint(http_client, sheet_data)

    assert response.status_code == 200

    response_data = response.json()

    assert CREATED_ID_KEY in response_data

    fetched_sheet = db_session.get(Sheet, response_data[CREATED_ID_KEY])

    assert fetched_sheet is not None


def _create_sheet_using_endpoint(http_client, sheet_data):
    return http_client.post("/sheets/", json=sheet_data,)


@pytest.mark.parametrize(
    'sheet_data',
    [{COLUMNS_DATA_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "double"},
                         {CELL_NAME_KEY: "A", CELL_TYPE_KEY: "boolean"}]},  # Test Duplicate names

     {COLUMNS_DATA_KEY: [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "invalid"},
                         {CELL_NAME_KEY: "B", CELL_TYPE_KEY: "boolean"}]},  # Test Invalid type

     {"cols": [{CELL_NAME_KEY: "A", CELL_TYPE_KEY: "invalid"},
               {CELL_NAME_KEY: "B", CELL_TYPE_KEY: "boolean"}]},  # Test Columns key

     {},  # Invalid, empty dictionary
     "invalid_json_argument"
     ]
)
def test_create_invalid_sheet_endpoint(http_client, db_session, sheet_data):
    response = _create_sheet_using_endpoint(http_client, sheet_data)

    assert response.status_code >= 400

    response_data = response.json()

    assert CREATED_ID_KEY not in response_data
