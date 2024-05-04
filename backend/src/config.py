import logging.config
import os

CURRENT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

APP_NAME = "SpreadsheetManager"
DATABASE_NAME = "spreadsheet"

DATABASE_USER = "spreadsheet_manager"
DATABASE_PASSWORD = "123"

# Configure logging
logging.config.fileConfig(os.path.join(CURRENT_FOLDER_PATH, "logging.conf"))
