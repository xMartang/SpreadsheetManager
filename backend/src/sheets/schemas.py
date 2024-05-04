from pydantic import BaseModel, field_validator

from sheets.consts import COLUMNS_KEY


class CreateSheetRequest(BaseModel):
    columns: list

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    COLUMNS_KEY: [
                        {
                            "name": "A",
                            "type": "boolean"
                        },
                        {
                            "name": "B",
                            "type": "int"
                        },
                        {
                            "name": "C",
                            "type": "double"
                        },
                        {
                            "name": "D",
                            "type": "string"
                        }
                    ]
                }
            ]
        }
    }


class SetCellValueRequest(BaseModel):
    column_name: str
    row_index: int
    value: str

    @field_validator('row_index')
    @classmethod
    def validate_row_index(cls, value: int):
        if value <= 0:
            raise ValueError("Row index value must be greater than 0...")

        return value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "column_name": "A",
                    "row_index": 11,
                    "value": "True"
                },
                {
                    "column_name": "B",
                    "row_index": 1,
                    "value": 21
                },
                {
                    "column_name": "C",
                    "row_index": 2,
                    "value": 1.337
                },
                {
                    "column_name": "D",
                    "row_index": 3,
                    "value": "lookup(A,11)"
                }
            ]
        }
    }
