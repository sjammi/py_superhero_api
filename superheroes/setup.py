#!/usr/bin/env python

import logging
from .utils.db import DBInterface
from .utils.hero_api import APIHandler
from .utils.parser import HeroParser

FORMAT = " %(name)s :: %(levelname)-8s :: %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


def setup_db(db):
    db.create_all_tables()
    logging.info("DB and tables created.")


def fill_db(db):
    handler = APIHandler()
    parser = HeroParser()
    raw_heroes = handler.query_api("all")
    parsed_heroes = parser.parse_raw_response("all", raw_heroes)
    heroes = []
    stats = []
    affiliations = []
    for hero in parsed_heroes:
        heroes.append(hero["hero"])
        stats.append(hero["stats"])
        affiliations.extend(hero["affiliation"])

    db.write("hero", heroes)
    db.write("hero_stats", stats)
    db.write("hero_affiliation", affiliations)


def setup():
    db = DBInterface()
    setup_db(db)
    fill_db(db)
