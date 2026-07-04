from sqlmodel import SQLModel

from app.models.hero_model import HeroBase
from app.models.team_model import TeamBase


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    password: str


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    password: str | None = None
    team_id: int | None = None


class TeamPublic(TeamBase):
    id: int


class TeamCreate(TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None
