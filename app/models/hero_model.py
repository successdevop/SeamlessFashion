from types import NoneType
from typing import Optional

from sqlmodel import SQLModel, Field, create_engine, Session, select, col, Relationship, text


class HeroTeamLink(SQLModel, table=True):
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id", primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    teams: list[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)


sqlite_file_name = "../database/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team=team_z_force
        )
        hero_rusty_man = Hero(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)

        hero_spider_boy.team = team_preventers
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("Updated hero:", hero_spider_boy)

        hero_black_lion = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")
        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            heroes=[hero_black_lion, hero_sure_e],
        )
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        print("Team Wakaland:", team_wakaland)

        hero_tarantula = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
        hero_dr_weird = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
        hero_cap = Hero(
            name="Captain North America", secret_name="Esteban Rogelios", age=93
        )

        team_preventers.heroes.append(hero_tarantula)
        team_preventers.heroes.append(hero_dr_weird)
        team_preventers.heroes.append(hero_cap)
        session.add(team_preventers)
        session.commit()
        session.refresh(hero_tarantula)
        session.refresh(hero_dr_weird)
        session.refresh(hero_cap)
        print("Preventers new hero:", hero_tarantula)
        print("Preventers new hero:", hero_dr_weird)
        print("Preventers new hero:", hero_cap)


def select_one():
    # with Session(engine) as session:
    #     result = session.exec(
    #         select(Hero).where(col(Hero.age) > 32).offset(1).limit(2)
    #     )
    #     print(result.all())
    with Session(engine) as session:
        hero = session.exec(
            select(Hero).where(Hero.name == "Spider Boy")
        ).one()
        print("================")
        print(hero)
        print("================")

        print("Spider Boy team: ", hero.team)

        team = session.exec(
            select(Team).where(Team.name == "Preventers")
        ).one()

        print("Team heroes: ", team.heroes)

        hero.team = team
        session.add(hero)
        session.commit()
        session.refresh(hero)

        hero.team = None
        session.add(hero)
        session.commit()
        session.refresh(hero)


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_1 = results.one()
        print("Hero 1:", hero_1)

        preventers = session.exec(
            select(Team).where(Team.name == "Preventers")
        ).one()

        hero_1.team = None

        print("Hero: ", hero_1)
        print("Preventers: ", preventers)
        print("Preventers Team Heroes: ", preventers.heroes)


def delete_heroes():
    with Session(engine) as session:
        hero = session.exec(
            select(Hero).where(Hero.team_id == 3)
        ).first()

        session.delete(hero)
        session.commit()
        print("Deleted team: ", hero)


def select_heroes_with_joint_table():
    with Session(engine) as session:
        # result = session.exec(
        #     select(Hero, Team).where(Hero.team_id == Team.id)
        # )
        #
        # for hero, team in result:
        #     print("Hero: ", hero, "|| Team: ", team)

        rslt = session.exec(
            select(Hero, Team).join(Team, isouter=True)
        )

        for hero, team in rslt:
            print("Hero: ", hero, "|| Team: ", team)


def update_hero_with_joint_table():
    with Session(engine) as session:
        obj = session.exec(
            select(Hero, Team).join(Team, isouter=True)
        ).all()

        hero_list = []
        team_list = []

        if obj is not None:
            for hero, team in obj:
                if not isinstance(hero, NoneType) and hero.name == "Spider Boy":
                    if len(hero_list) < 1:
                        hero_list.append(hero)
                if not isinstance(team, NoneType) and team.name == "Preventers":
                    if len(team_list) < 1:
                        team_list.append(team)
                if len(hero_list) == 1 and len(team_list) == 1:
                    break

        hero_1 = hero_list[0]
        team_1 = team_list[0]
        hero_1.team_id = team_1.id

        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)


def remove_hero_with_joint_table():
    with Session(engine) as session:
        obj = session.exec(
            select(Hero, Team).join(Team, isouter=True)
        ).all()

        if obj is not None:
            for hero, _ in obj:
                if not isinstance(hero, NoneType) and hero.name == "Spider Boy":
                    hero.team_id = None
                    session.add(hero)
                    session.commit()
                    session.refresh(hero)
                    break


def main():
    # create_db_and_tables()
    # create_heroes()
    # select_one()
    # update_heroes()
    delete_heroes()
    # select_heroes_with_joint_table()
    # update_hero_with_joint_table()
    # remove_hero_with_joint_table()


if __name__ == "__main__":
    main()
