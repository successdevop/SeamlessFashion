from fastapi import FastAPI
from contextlib import asynccontextmanager

from sqlmodel import Session, select

from app.models.hero_model import create_db_and_tables, engine, Hero
from app.schemas.hero_schema import HeroPublic, HeroCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("==============================")
    print("Server is starting.....")
    print("==============================")
    create_db_and_tables()
    print("==============================")
    print("Database created.....")
    print("==============================")
    yield
    print("==============================")
    print("Server has been stopped.....")
    print("==============================")
    engine.dispose()
    print("==============================")
    print("Server connection closed")
    print("==============================")


app = FastAPI(
    lifespan=lifespan
)


@app.post("/heroes", response_model=HeroPublic)
def create_heroes(hero: HeroCreate):
    with Session(engine) as session:
        db_hero = Hero.model_validate(hero)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero


@app.get("/heroes", response_model=list[HeroPublic])
def get_heroes():
    with Session(engine) as session:
        all_heroes = session.exec(
            select(Hero)
        ).all()

        return all_heroes

