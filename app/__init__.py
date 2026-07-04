from fastapi import FastAPI, HTTPException, status, Query
from contextlib import asynccontextmanager

from sqlmodel import Session, select

from app.models.hero_model import create_db_and_tables, engine, Hero
from app.schemas.hero_schema import HeroPublic, HeroCreate, HeroUpdate


@asynccontextmanager
async def lifespan(my_app: FastAPI):
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

def hash_password(password: str):
    return f"not really hashed {password} hehehe"


@app.post("/heroes", response_model=HeroPublic, status_code=status.HTTP_200_OK)
def create_heroes(hero: HeroCreate):
    hashed_password = hash_password(hero.password)
    with Session(engine) as session:
        db_hero = Hero.model_validate(hero, update={"hashed_password": hashed_password})
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero


@app.get("/heroes", response_model=list[HeroPublic], status_code=status.HTTP_200_OK)
def read_heroes(offset: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as session:
        all_heroes = session.exec(
            select(Hero).offset(offset).limit(limit)
        ).all()

        return all_heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublic, status_code=status.HTTP_200_OK)
def read_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return hero


@app.patch("/heroes/{hero_id}", response_model=HeroPublic, status_code=status.HTTP_200_OK)
def update_hero(hero_id: int, hero: HeroUpdate):
    with Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        if not db_hero:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

        new_db_hero = hero.model_dump(exclude_unset=True)

        extra_data = {}
        if "password" in new_db_hero:
           extra_data["hashed_password"] = hash_password(new_db_hero["password"])
        new_db_hero.update(extra_data)

        for k, v in new_db_hero.items():
            setattr(db_hero, k, v)

        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero

