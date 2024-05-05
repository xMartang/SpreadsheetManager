# SpreadsheetManager
My implementation for the spreadsheet manager task, using fastapi and postgresql.

## Assumptions
Here are all the assumptions I made and ended up in my implementation.
hopefully it still meets your requirements :)

1. The column names in each sheet are unique, if they won't be unique the lookup function won't work properly.
2. Column type ignores letter case.
3. Sheets can be empty (with 0 columns).

## Usage 
Here's a guide on how to setup and use this spreadsheet manager:

### Install python requirements
If you are using linux, just run the `install_requirements.sh` script found in the top project folder.
Otherwise, open a console in this folder and run "python3 -m pip install -r backend/requirements.txt".

### Database Setup
Make sure you have postgresql installed before proceeding.

If you are using linux, just run the `setup_databases.sh` script found in the top project folder.
Otherwise, follow the steps bellow:

1. Create a postgresql user named spreadsheet_manager with the password '123'.
2. Add createdb permissions for the user.
3. Create two databases:
   * For production, create a database named `spreadsheet`
   * For testing, create a database named `test_spreadsheet`
4. Open a console in the 'backend' folder and run `alembic upgrade head` to ensure that you are using the latest revision.

NOTE: If you decide to use a different username/password/database name, make sure to rename them in the sqlalchemy 
database connection url in the `backend/alembic.ini`, under `sqlalchemy.url`.

### Start Server
To start the server, simply open a console in the 'backed/src' folder and run `uvicorn main:app --reload`.

### Testing
The tests were written using pytest, I recommend running pytest with the following command:

`pytest --cov=/path/to/spreadsheet/manager/backend/src --cov-report term-missing`

To only run the unit tests, run the command from the 'backend/tests/unit' directory.

To only run the integration tests, run the command from the 'backend/tests/unit' directory.

To run both at the same time, run the command from the 'backend/tests' directory.

