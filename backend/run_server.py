import os
import sys
from subprocess import check_call
from configparser import ConfigParser
from alembic import command

import uvicorn
from dotenv import load_dotenv

from src.config import APP_FOLDER_PATH

load_dotenv(".env")

DB_NAME = os.environ['POSTGRES_DB']
DB_USERNAME = os.environ['POSTGRES_USER']
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']

SQLALCHEMY_CONNECTION_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}"


def _set_db_url(sqlalchemy_url=SQLALCHEMY_CONNECTION_URL):
    alembic_config_parser = ConfigParser()
    alembic_config_parser.read("alembic.ini")

    alembic_config_parser.set('alembic', "sqlalchemy.url", sqlalchemy_url)


def _set_db_revision_to_latest():
    check_call(["alembic", "upgrade", "head"])


def db_setup():
    _set_db_url()
    _set_db_revision_to_latest()


def run_server():
    db_setup()

    sys.path.insert(0, APP_FOLDER_PATH)

    uvicorn.run(
        "main:app",
        reload=True,
        port=int(os.environ.get("BACKEND_SERVER_PORT", 8000)),
        reload_dirs=['src']
    )


if __name__ == "__main__":
    run_server()
