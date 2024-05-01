#!/bin/sh

# Create the database and the user that will be using it
sudo -u postgres bash -c "psql -c \"CREATE USER spreadsheet_manager WITH PASSWORD '123';\""
sudo -u postgres createdb spreadsheet
sudo -u postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE spreadsheet TO spreadsheet_manager;\""
