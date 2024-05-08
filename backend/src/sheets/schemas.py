from pydantic import BaseModel, field_validator

from sheets.consts import COLUMNS_KEY

SHEET_REQUEST_VALUE_EXAMPLE = {
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


class CreateSheetRequest(BaseModel):
    columns: list

    model_config = {
        "json_schema_extra": {
            "examples": [
                SHEET_REQUEST_VALUE_EXAMPLE
            ]
        }
    }


class GetSheetResponse(BaseModel):
    sheet_data: dict

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sheet_data": {
                        "columns": [
                            {
                                "name": "A",
                                "type": "string",
                                "cells": [
                                    {
                                        "row_index": 10,
                                        "value": "hello"
                                    }
                                ]
                            },
                            {
                                "name": "B",
                                "type": "boolean",
                                "cells": [
                                    {
                                        "row_index": 8,
                                        "value": 0
                                    },
                                    {
                                        "row_index": 11,
                                        "value": 1
                                    }
                                ]
                            },
                            {
                                "name": "C",
                                "type": "string",
                                "cells": [
                                    {
                                        "row_index": 1,
                                        "value": "hello"
                                    }
                                ]
                            }
                        ]
                    }
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
            ]
        }
    }


class SetCellValueResponse(BaseModel):
    cell_id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cell_id": 11,
                },
            ]
        }
    }
