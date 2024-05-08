## SpreadsheetManager API docs

* Please refer http://localhost:8000/docs/ for documentation and live examples
------------------------------------------------------------------------------------------

#### Create sheet : POST Request -> http://localhost:8000/sheets



##### Example cURL

> ```javascript
>  curl -X POST -H "Content-Type: application/json" --data '{json_data}' http://localhost:8000/sheets
> ```

##### Data Schema

```
  {
    columns": [
      {
        "name": String,
        "type": String
      }
    ]
  }
```

##### Example Json Data

```
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
```

##### Responses

> | http code | content-type           | Description                          |
> |-----------|------------------------|--------------------------------------|
> | `201`     | `application/json`     | `{"sheet_id": {created_sheet_id}`    |
> | `400`     | `application/json`     | `{"detail": "invalid_data_message"}` |
> | `422`     | `application/json`     | `Validation Error`                   | 


------------------------------------------------------------------------------------------

#### Get Sheet By Id : GET Request -> http://localhost:8000/sheets/{sheet_id}/

##### Example cURL

> ```javascript
>  curl -X GET -H "Content-Type: application/json" http://localhost:8000/sheets/1/
> ```

##### Responses

> | http code  | content-type        |
> |------------|---------------------|
> | `200`      | `application/json`  |


##### Example Response

```
  {
    "sheet_data": {
      "columns": [
        {
          "cells": [
            {
              "row_index": 10,
              "value": "hello"
            }
          ],
          "name": "A",
          "type": "string"
        },
        {
          "cells": [
            {
              "row_index": 8,
              "value": 0
            },
            {
              "row_index": 11,
              "value": 1
            }
          ],
          "name": "B",
          "type": "boolean"
        },
        {
          "cells": [],
          "name": "C",
          "type": "string"
        }
      ]
    }
  }
```


------------------------------------------------------------------------------------------

#### Set Cell Value : POST Request -> http://localhost:8000/sheets/{sheet_id}/set_cell_value

##### Example cURL

> ```javascript
>  curl -X POST -H "Content-Type: application/json" --data '{json_data}' http://localhost:8000/sheets/{sheet_id}/set_cell_value
> ```

##### Data Schema

```
  {
    "column_name": String,
    "row_index": Integer,
    "value": String
  }
```

##### Example Json Data

###### Boolean Example

```
  {
    "column_name": "A",
    "row_index": 11,
    "value": "True"
  }
```

###### Integer Example

```
  {
    "column_name": "B",
    "row_index": 4,
    "value": "1"
  }
```


###### Double Example

```
  {
    "column_name": "C",
    "row_index": 4,
    "value": "1.337"
  }
```

###### Lookup Example

```
  {
    "column_name": "A",
    "row_index": 4,
    "value": "lookup(A,11)"
  }
```

##### Responses

> | http code | content-type            | response                             |
> |-----------|-------------------------|--------------------------------------|
> | `200`     | `application/json`      | `{"cell_id": 11}`                    |
> | `400`     | `application/json`      | `{"detail": "invalid_data_message"}` |
> | `422`     | `application/json`      | `Validation Error`                   |
