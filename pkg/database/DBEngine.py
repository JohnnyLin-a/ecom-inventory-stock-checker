from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os

class DBEngine:
    __db: Engine

    def __init__(self):
        db_string = "postgres://" + os.getenv("POSTGRES_USER") + ":" + os.getenv("POSTGRES_PASSWORD") + "@" + os.getenv("POSTGRES_HOST") + ":" + os.getenv("POSTGRES_PORT") + "/" + os.getenv("POSTGRES_DB")
        self.__db = create_engine(db_string)

    def get(self) -> Engine:
        return self.__db