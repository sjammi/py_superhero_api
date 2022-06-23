import logging

from sqlalchemy import (
    create_engine,
    Column,
    Boolean,
    Integer,
    String,
    ForeignKey,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database


DeclarativeBase = declarative_base()


def db_connect():
    """
    Returns sqlalchemy engine instance
    """
    engine = create_engine("postgresql://localhost/superheroes")
    if not database_exists(engine.url):
        logging.info("Creating DB.")
        create_database(engine.url)

    return engine


def create_all_tables(engine):
    logging.info("Creating Tables.")
    DeclarativeBase.metadata.create_all(engine)


def write_to_db(engine, table, data):
    s = Session(bind=engine)
    
    s.bulk_insert_mappings(

    )


class Hero(DeclarativeBase):
    __tablename__ = "hero"

    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=True)
    alias = Column("alias", String, nullable=True)
    species = Column("species", String, nullable=True)
    first_appearance = Column("first_appearance", String, nullable=True)
    publisher = Column("publisher", String, nullable=True)


class HeroStats(DeclarativeBase):
    __tablename__ = "hero_stats"

    id = Column(Integer, ForeignKey("hero.id"), primary_key=True)
    intelligence = Column("intelligence", Integer, nullable=True)
    strength = Column("strength", Integer, nullable=True)
    speed = Column("speed", Integer, nullable=True)
    durability = Column("durability", Integer, nullable=True)
    power = Column("power", Integer, nullable=True)
    combat = Column("combat", Integer, nullable=True)


class HeroAffiliation(DeclarativeBase):
    __tablename__ = "hero_affiliation"

    id = Column(Integer, ForeignKey("hero.id"), primary_key=True)
    affiliation = Column("affiliation", String, nullable=True)


hero_name_idx = Index("hero_name_idx", Hero.alias)
hero_affiliation_idx = Index("hero_affiliation_idx", HeroAffiliation.affiliation)
