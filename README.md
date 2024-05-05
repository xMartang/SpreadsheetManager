# SpreadsheetManager

My implementation for the spreadsheet manager task, using fastapi and postgresql

## Assumptions

Here are all the assumptions I made and ended up in my implementation.
hopefully it still meets your requirements :)

1. The cell names are unique and cannot be empty, if they won't be unique the lookup function won't work properly.
2. Cell type ignores letter case.
3. Sheets can be empty (with 0 cells).

## Usage 
Here's a guide on how to setup and use this spreadsheet manager:

### Install python requirements
If you are using linux, just run the `install_requirements.sh` script found in the top project folder.
Otherwise, open a console in this folder and run "python3 -m pip install -r backend/requirements.txt".

### Database Setup
If you are using linux, just run the `setup_databases.sh` script found in the top project folder.
Otherwise, follow the steps bellow:

1. Create a postgresql user named spreadsheet_manager with the password '123'.
2. Add createdb permissions for the user.
3. Create two databases:
   * For production, create a database named `spreadsheet`
   * For testing, create a database named `test_spreadsheet`
4. Open a console in the 'backend' folder and run `alembic upgrade head` to ensure that you use the latest revision.

NOTE: If you decide to use a different user or a different database name, make sure to rename the sqlalchemy database 
connection url in the `backend/alembic.ini`, under `sqlalchemy.url`

### Start Server
To start the server, simply open a console in the 'backed/src' folder and run `uvicorn main:app --reload`.

### Testing
The tests were written using pytest, I recommend running pytest with the following command in order to also see code
coverage in the tests:

`pytest --cov=/path/to/spreadsheet/manager/backend/src --cov-report term-missing`

