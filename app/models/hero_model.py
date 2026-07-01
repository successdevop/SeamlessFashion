from types import NoneType
from typing import Optional

from sqlmodel import SQLModel, Field, create_engine, Session, select, col, Relationship


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")


sqlite_file_name = "../database/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Towers")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", team=team_preventers)
        hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_z_force)
        hero_spider_boy = Hero(name="Spider Boy", secret_name="Pedro Parqueador")

        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()
        #
        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)
        #
        print("Created hero: ", hero_deadpond)
        print("Created hero: ", hero_rusty_man)
        print("Created hero: ", hero_spider_boy)


def select_one():
    with Session(engine) as session:
        result = session.exec(
            select(Hero).where(col(Hero.age) > 32).offset(1).limit(2)
        )
        print(result.all())


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_1 = results.one()
        print("Hero 1:", hero_1)

        statement = select(Hero).where(Hero.name == "Captain North America")
        results = session.exec(statement)
        hero_2 = results.one()
        print("Hero 2:", hero_2)

        hero_1.age = 16
        hero_1.name = "Spider-Youngster"
        session.add(hero_1)

        hero_2.name = "Captain North America Except Canada"
        hero_2.age = 110
        session.add(hero_2)

        session.commit()
        session.refresh(hero_1)
        session.refresh(hero_2)

        print("Updated hero 1:", hero_1)
        print("Updated hero 2:", hero_2)


def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.one()
        print("Hero: ", hero)

        session.delete(hero)
        session.commit()

        print("Deleted hero:", hero)

        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.first()

        if hero is None:
            print("There's no hero named Spider-Youngster")


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
    create_heroes()
    # select_one()
    # update_heroes()
    # delete_heroes()
    # select_heroes_with_joint_table()
    # update_hero_with_joint_table()
    # remove_hero_with_joint_table()


if __name__ == "__main__":
    main()
