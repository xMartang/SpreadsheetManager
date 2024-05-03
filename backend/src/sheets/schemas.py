
from pydantic import BaseModel


class CreateSheetRequest(BaseModel):
    columns: list

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "columns": [
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
    name: str
    value: str
