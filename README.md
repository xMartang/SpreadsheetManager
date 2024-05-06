# SpreadsheetManager
My implementation for the spreadsheet manager task, using fastapi and postgresql

## Assumptions
Here are all the assumptions I made and ended up in my implementation.
hopefully it still meets your requirements :)

1. The column names in each sheet are unique, if they won't be unique the lookup function won't work properly.
2. Column type ignores letter case.
3. Sheets can be empty (with 0 columns).

## Usage 
Here's a guide on how to setup and use this spreadsheet manager:

### Quickstart
There are two ways to start the server.

* Dockers:
1. Build the dockers by running `docker-compose build`
2. Run the server by running `docker-compose up -d`

* Standalone (for debugging):
1. Install the python requirements for the project (follow `Install python requirements` bellow).
2. Start the database docker by running `docker-compose up -d db`
3. Run the server by running the `run_server.py` script in the 'backend' folder

### Install python requirements
If you are using linux, just run the `install_requirements.sh` script found in the top project folder.
Otherwise, open a console in the 'backend' folder and run `python3 -m pip install -r requirements.txt`.

### Testing
To run the tests:
* Make sure that you have all python project requirements installed (if you don't, follow `Install python requirements` above)

1. Open a console in the 'backend/tests' directory.
2. Install the python test requirements by running `python3 -m pip install -r test_requirements.txt`.
3. Use the following commands to run the tests:

* Command for unit tests: `pytest --cov=../src --cov-report term-missing unit`

* Command for integration tests: `pytest --cov=../src --cov-report term-missing integration`

* Command for both: `pytest --cov=../src --cov-report term-missing`

NOTE: make sure that the `test_db` service inside the 'docker-compose.yml' file is running (`docker-compose up -d test_db`),
otherwise the tests won't work.
