from typing import Optional

from sqlmodel import SQLModel, Field, create_engine, Session, select, col, Relationship, text


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


__sqlite_file_name = "database.db"
__sqlite_url = f"sqlite:///{__sqlite_file_name}"

__context_args = {"check_same_thread": False, "timeout":5}
engine = create_engine(__sqlite_url, echo=True, connect_args=__context_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))
