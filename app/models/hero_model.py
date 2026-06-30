from typing import Optional

from sqlmodel import SQLModel, Field, create_engine, Session, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = "../database/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_heroes():
    hero1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero3 = Hero(name="Rusty-man", secret_name="Tommy Sharp", age=48)

    with Session(engine) as session:
        session.add(hero1)
        session.add(hero2)
        session.add(hero3)

        session.commit()

def select_heroes():
    with Session(engine) as session:
        statement = select(Hero)
        result = session.exec(statement)
        heroes = result.all()
        print(result)
        print(heroes)
        
        if result is not None:
            for hero in result:
                print(hero)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()

if __name__ == "__main__":
    main()