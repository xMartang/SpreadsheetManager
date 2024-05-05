import logging.config
import os
from configparser import ConfigParser

config_parser = ConfigParser()

# General
APP_NAME = "SpreadsheetManager"
CURRENT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

# Database
ALEMBIC_DATABASE_CONFIG_FILE_PATH = os.path.join(CURRENT_FOLDER_PATH, "..", "alembic.ini")
config_parser.read(ALEMBIC_DATABASE_CONFIG_FILE_PATH)

SQL_ALCHEMY_DATABASE_CONNECTION_URL = config_parser.get('alembic', "sqlalchemy.url")
DATABASE_NAME = SQL_ALCHEMY_DATABASE_CONNECTION_URL.rsplit("/", 1)[1]

# Logging
os.makedirs("logs", exist_ok=True)
logging.config.fileConfig(os.path.join(CURRENT_FOLDER_PATH, "logging.conf"))
