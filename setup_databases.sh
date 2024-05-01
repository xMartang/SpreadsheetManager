#!/bin/sh

# Create the database user and give him permissions to create databases
sudo -i -u postgres bash -c "psql -c \"CREATE USER spreadsheet_manager WITH PASSWORD '123';\""
sudo -i -u postgres bash -c "psql -c \"ALTER USER spreadsheet_manager WITH CREATEDB;\""

# Create the databases
sudo -i -u spreadsheet_manager createdb spreadsheet
sudo -i -u spreadsheet_manager createdb spreadsheet_test

# Make sure that we are running with the latest database revision using alembic
cd backend
alembic upgrade head

