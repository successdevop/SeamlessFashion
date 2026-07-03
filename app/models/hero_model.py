from types import NoneType
from typing import Optional

from sqlmodel import SQLModel, Field, create_engine, Session, select, col, Relationship, text


class HeroTeamLink(SQLModel, table=True):
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id", primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)

    is_training: bool = False

    team: "Team" = Relationship(back_populates="hero_links")
    hero: "Hero" = Relationship(back_populates="team_links")


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    hero_links: list[HeroTeamLink] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_links: list[HeroTeamLink] = Relationship(back_populates="hero")


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
            name="Deadpond", secret_name="Dive Wilson"
        )
        hero_rusty_man = Hero(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")

        deadpond_team_z_link = HeroTeamLink(team=team_z_force, hero=hero_deadpond)
        deadpond_preventers_link = HeroTeamLink(team=team_preventers, hero=hero_deadpond, is_training=True)

        spider_boy_preventers_link = HeroTeamLink(team=team_preventers, hero=hero_spider_boy, is_training=True)
        rusty_man_preventers_link = HeroTeamLink(team=team_preventers, hero=hero_rusty_man)

        session.add(deadpond_team_z_link)
        session.add(deadpond_preventers_link)
        session.add(spider_boy_preventers_link)
        session.add(rusty_man_preventers_link)
        session.commit()

        for link in team_z_force.hero_links:
            print("Z-Force hero: ", link.hero, "is training: ", link.is_training)

        for link in team_preventers.hero_links:
            print("Preventers hero: ", link.hero, "is training: ", link.is_training)


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
        # team_z_force = session.exec(
        #     select(Team).where(Team.name == "Z-Force")
        # ).one()

        spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()

        # spider_boy_z_force_link = HeroTeamLink(team=team_z_force, hero=spider_boy)
        #
        # spider_boy.team_links.append(spider_boy_z_force_link)
        # session.add(spider_boy)
        # session.commit()

        for link in spider_boy.team_links:
            if link.team.name == "Preventers":
                link.is_training = False
        session.add(spider_boy)
        session.commit()

        for link in spider_boy.team_links:
            print(f"Spider-Boy team: {link.team.name}", f" is training: {link.is_training}")


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
    update_heroes()
    # delete_heroes()
    # select_heroes_with_joint_table()
    # update_hero_with_joint_table()
    # remove_hero_with_joint_table()


if __name__ == "__main__":
    main()
