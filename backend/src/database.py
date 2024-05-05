import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from config import SQL_ALCHEMY_DATABASE_CONNECTION_URL, DATABASE_NAME
from design_patterns.singleton import SingletonMeta


class Base(DeclarativeBase):

    @property
    def blacklisted_json_columns(self):
        return ["id"]

    def to_json(self):
        return {
            column_name: getattr(self, column_name) for column_name in self.__table__.columns.keys()
            if column_name not in self.blacklisted_json_columns
        }


class Database(metaclass=SingletonMeta):

    def __init__(self, sql_alchemy_url=SQL_ALCHEMY_DATABASE_CONNECTION_URL):
        self.engine = create_engine(sql_alchemy_url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


def ensure_database_exists():
    engine = Database().engine

    if not database_exists(engine.url):
        logging.debug(f"Creating database '{DATABASE_NAME}' with url '{SQL_ALCHEMY_DATABASE_CONNECTION_URL}'")

        create_database(engine.url)

        # Create all tables in database
        Base.metadata.create_all(engine)


def get_db():
    db = Database().session_local()

    try:
        yield db
    finally:
        db.close()
