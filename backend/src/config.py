import logging.config
import os
from configparser import ConfigParser

config_parser = ConfigParser()

# General
APP_NAME = "SpreadsheetManager"
APP_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DEBUG_MODE = False

# Database
ALEMBIC_DATABASE_CONFIG_FILE_PATH = os.path.join(APP_FOLDER_PATH, "..", "alembic.ini")
config_parser.read(ALEMBIC_DATABASE_CONFIG_FILE_PATH)

SQL_ALCHEMY_DATABASE_CONNECTION_URL = config_parser.get('alembic', "sqlalchemy.url")
DATABASE_NAME = SQL_ALCHEMY_DATABASE_CONNECTION_URL.rsplit("/", 1)[1]

# Logging
LOGS_PATH = os.path.abspath(os.path.join(APP_FOLDER_PATH, "..", "logs"))
os.makedirs(LOGS_PATH, exist_ok=True)
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - [%(levelname)-8s] -- %(message)s'
        },
        'complex': {
            'format': '%(asctime)s - [%(levelname)-8s] --- %(module)-17s : %(lineno)d - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'complex',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_PATH, 'server.log'),
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'uvicorn': {
            'level': 'INFO',
            'propagate': True
        },
    }
})
