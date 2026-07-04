from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, create_engine, text, Relationship

if TYPE_CHECKING:
    from app.models import Team


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    team_id: int | None = Field(default=None, foreign_key="team.id", ondelete="CASCADE")


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field()

    team: "Team" = Relationship(back_populates="heroes")


__sqlite_file_name = "database.db"
__sqlite_url = f"sqlite:///{__sqlite_file_name}"

__context_args = {"check_same_thread": False, "timeout":5}
engine = create_engine(__sqlite_url, echo=True, connect_args=__context_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))
