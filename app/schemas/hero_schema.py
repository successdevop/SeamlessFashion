from sqlmodel import SQLModel

from app.models.hero_model import HeroBase


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    password: str


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    password: str | None = None