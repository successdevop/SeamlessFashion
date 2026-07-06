from fastapi import FastAPI, HTTPException, status, Query, Depends
from contextlib import asynccontextmanager

from sqlmodel import Session, select

from app.models import Team, Hero
from app.models.hero_model import create_db_and_tables, engine
from app.schemas.hero_schema import HeroPublic, HeroCreate, HeroUpdate, TeamPublic, TeamCreate, TeamUpdate, \
    HeroPublicWithTeam, TeamPublicWithHeroes


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


def get_db_session():
    with Session(engine) as session:
        yield session


def hash_password(password: str):
    return f"not really hashed {password} hehehe"


@app.post("/heroes", response_model=HeroPublic, status_code=status.HTTP_201_CREATED)
def create_heroes(*, session: Session = Depends(get_db_session), hero: HeroCreate):
    hashed_password = hash_password(hero.password)

    db_hero = Hero.model_validate(hero, update={"hashed_password": hashed_password})
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes", response_model=list[HeroPublic], status_code=status.HTTP_200_OK)
def read_heroes(*, session: Session = Depends(get_db_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    all_heroes = session.exec(
        select(Hero).offset(offset).limit(limit)
    ).all()

    return all_heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublicWithTeam, status_code=status.HTTP_200_OK)
def read_hero(*, session: Session = Depends(get_db_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroPublic, status_code=status.HTTP_200_OK)
def update_hero(*, session: Session = Depends(get_db_session), hero_id: int, hero: HeroUpdate):
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


@app.delete("/heroes/{hero_id}", response_model=dict[str, str], status_code=status.HTTP_200_OK)
def delete_hero(*, session: Session = Depends(get_db_session), hero_id: int):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    session.delete(db_hero)
    session.commit()
    return {"detail": "Deleted successfully"}


@app.post("/teams", response_model=TeamPublic, status_code=status.HTTP_201_CREATED)
def create_team(*, session: Session = Depends(get_db_session), team: TeamCreate):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get("/teams", response_model=list[TeamPublic], status_code=status.HTTP_200_OK)
def read_teams(*, session: Session = Depends(get_db_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    all_teams = session.exec(
        select(Team).offset(offset).limit(limit)
    ).all()

    return all_teams


@app.get("/teams/{team_id}", response_model=TeamPublicWithHeroes, status_code=status.HTTP_200_OK)
def read_team(*, session: Session = Depends(get_db_session), team_id: int):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return db_team


@app.patch("/teams/{team_id}", response_model=TeamPublic, status_code=status.HTTP_200_OK)
def update_team(team_id: int, team_req: TeamUpdate, session: Session = Depends(get_db_session)):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    team_data = team_req.model_dump(exclude_unset=True)
    for k, v in team_data.items():
        setattr(db_team, k, v)

    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.delete("/teams/{team_id}", response_model=dict[str, bool], status_code=status.HTTP_200_OK)
def delete_team(team_id: int, session: Session = Depends(get_db_session)):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    session.delete(db_team)
    session.commit()

    return {"deleted": True}
