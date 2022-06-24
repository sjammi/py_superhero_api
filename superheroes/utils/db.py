import logging
from typing import List, Dict

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Index,
    MetaData,
    func,
    text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy_utils import database_exists, create_database


DeclarativeBase = declarative_base()


class Hero(DeclarativeBase):
    __tablename__ = "hero"

    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=True)
    alias = Column("alias", String, nullable=True)
    species = Column("species", String, nullable=True)
    first_appearance = Column("first_appearance", String, nullable=True)
    publisher = Column("publisher", String, nullable=True)

    stats = relationship(
        "HeroStats",
        cascade="all, delete",
        passive_deletes=True,
    )
    affiliations = relationship(
        "HeroAffiliation",
        cascade="all, delete",
        passive_deletes=True,
    )


class HeroStats(DeclarativeBase):
    __tablename__ = "hero_stats"

    id = Column(Integer, ForeignKey("hero.id", ondelete="CASCADE"), primary_key=True)
    intelligence = Column("intelligence", Integer, nullable=True)
    strength = Column("strength", Integer, nullable=True)
    speed = Column("speed", Integer, nullable=True)
    durability = Column("durability", Integer, nullable=True)
    power = Column("power", Integer, nullable=True)
    combat = Column("combat", Integer, nullable=True)


class HeroAffiliation(DeclarativeBase):
    __tablename__ = "hero_affiliation"

    id = Column(Integer, ForeignKey("hero.id", ondelete="CASCADE"), primary_key=True)
    affiliation = Column("affiliation", String, primary_key=True)

hero_name_idx = Index("hero_name_idx", func.lower(Hero.alias))
hero_affiliation_idx = Index("hero_affiliation_idx", func.lower(HeroAffiliation.affiliation))


table_type_map = {
    "hero": Hero,
    "hero_stats": HeroStats,
    "hero_affiliation": HeroAffiliation
}

class DBInterface():
    def __init__(self):
        """
        Sets sqlalchemy engine instance
        """
        engine = create_engine("postgresql://localhost/superheroes")
        if not database_exists(engine.url):
            logging.info("Creating DB.")
            create_database(engine.url)

        self.engine = engine
        self.metadata = MetaData(bind=engine)
        MetaData.reflect(self.metadata)

    def create_all_tables(self):
        logging.info("Creating Tables.")
        DeclarativeBase.metadata.create_all(self.engine)

    def write(self, table, data):
        if table not in table_type_map.keys():
            raise Exception(f"Invalid table name given for write. Please provide one of the following: {table_type_map.keys()}")

        s = Session(bind=self.engine)
        s.bulk_insert_mappings(
            table_type_map[table],
            data
        )
        s.commit()
        logging.info(f"Wrote {len(data)} rows to {table}")
    
    def read(self, query) -> List[Dict]:
        data = []
        with self.engine.connect() as conn:
            query = text(query)
            logging.info(f"Running query: {query}")
            res = conn.execute(query)
            return [x for x in res]

    def delete(self, hero: str):
        """
        ?TODO: if multiple heroes have the same name, all get deleted. Short of delete by ID, not sure what the best option would be.
        """
        s = Session(bind=self.engine)
        s.query(Hero).filter(func.lower(Hero.alias) == func.lower(hero)).delete(synchronize_session=False)
        s.commit()
    
    def update(self, args: Dict):
        pass
