from sheets.consts import COLUMN_NAME_KEY, COLUMN_TYPE_KEY


def test_column_to_json_method(int_column):
    json_data = int_column.to_json()

    assert COLUMN_NAME_KEY in json_data
    assert COLUMN_TYPE_KEY in json_data


def test_cell_to_json_method(int_cell):
    json_data = int_cell.to_json()

    assert "row_index" in json_data
    assert "value" in json_data
