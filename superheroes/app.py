import logging
from json import dumps
from .db import db_connect, create_all_tables, write_to_db
from .hero_api import APIHandler, HeroParser

FORMAT = " %(name)s :: %(levelname)-8s :: %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


def health_check():
    logging.info("Check check check")


def setup_db():
    engine = db_connect()
    create_all_tables(engine)
    logging.info("DB and tables created.")


def load_data_from_api():
    handler = APIHandler()
    parser = HeroParser()
    hero = handler.query_api("id", 1)
    parsed_hero = parser.parse_raw_response("all", hero)
    print(dumps(parsed_hero, indent=1))


def fill_db():
    handler = APIHandler()
    parser = HeroParser()
    heroes = handler.query_api("all")
    parsed_hero = parser.parse_raw_response("all", heroes)
    # print(dumps(parsed_hero, indent=1))
