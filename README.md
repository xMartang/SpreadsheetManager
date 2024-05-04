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

### Database Setup
If you are using ubuntu, just run the `setup_databases.sh` script instead of the following manual work.

1. Create a postgresql user named spreadsheet_manager with the password '123'.
2. Add createdb permissions for the user.
3. Create two databases:
   * For production, create a database named `spreadsheet`
   * For testing, create a database named `test_spreadsheet`
4. Open a console in the backend folder and run `alembic upgrade head` to ensure that you use the latest revision.
