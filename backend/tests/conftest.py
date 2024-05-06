import os

from database import Database, ensure_database_exists

TEST_DATABASE_NAME = os.environ["POSTGRES_DB"]
DATABASE_PORT = os.environ["PGPORT"]
DATABASE_USER = os.environ["POSTGRES_USER"]
DATABASE_PASSWORD = os.environ["POSTGRES_PASSWORD"]

Database(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost:{DATABASE_PORT}/{TEST_DATABASE_NAME}')

# Create the test database if it doesn't exist
ensure_database_exists()


