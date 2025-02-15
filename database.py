from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import logging
import os
from sqlalchemy import event, Engine
import sqlite3

# Carregando as variáveis de ambiente
load_dotenv()

# Configurando o logger
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está definida no arquivo .env")

engine = create_engine(DATABASE_URL)

def create_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)


# Ativando foreign_keys para SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
