#!/usr/bin/env python

import logging
import uvicorn
from fastapi import FastAPI, Request

from .utils.db import DBInterface
from .utils.hero_api import HeroParser

FORMAT = " %(name)s :: %(levelname)-8s :: %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

app = FastAPI()
db = DBInterface()
parser = HeroParser()


@app.get("/health")
def health_check():
    return {"message": "Check check check"}


@app.get("/hero/{name}")
def get_hero(name):
    query = f"""
    select
        h.*,
        hs.*,
        ARRAY(select affiliation from hero_affiliation ha where ha.id = h.id) as affiliations
    from hero h
    left join hero_stats hs on h.id = hs.id
    where alias ilike '{name}';
    """
    res = db.read(query)
    return {"heroes": [ parser.parse_db_response(row) for row in res]}


@app.get("/team/{team}")
def get_team(team):
    """
    :param team - replace any spaces with %20, ex justice league -> /team/justice%20league
    """
    query = f"""
    select
        h.alias
    from hero_affiliation ha
    left join hero h on ha.id = h.id
    where ha.affiliation ilike '{team}';
    """
    res = db.read(query)
    return {team: [ h["alias"] for h in res]}

@app.get("/team/fuzzy/{name}")
def get_teams_fuzzy(name):
    """
    Returns any teams that are similar to a given name. Ex, "avengers" -> Avengers, New Avengers, Young Avengers, ...
    :param team - replace any spaces with %20, ex justice league -> /team/justice%20league
    """
    query = f"""
    with heroes_by_team as (
        select
            affiliation as team,
            array_agg(id) as member_ids
        from hero_affiliation
        where affiliation ilike '%{name}%'
        group by affiliation
    )
    select
        ht.team,
        ARRAY(select alias from hero h where h.id = ANY(ht.member_ids)) as members
    from heroes_by_team ht;
    """
    res = db.read(query)
    return { row["team"]: row["members"] for row in res }


@app.get("/hero/strongest/{stat}")
def get_strongest(stat):
    """
    Returns the 5 strongest heroes in a given stat
    :param stat - Expects a stat in the hero_stats table: [intelligence, strength, speed, durability, power, combat]
    """
    stat = stat.lower()
    query = f"""
    select
        h.alias,
        hs.{stat}
    from hero h
    left join hero_stats hs on h.id = hs.id
    order by hs.{stat} desc
    limit 5
    """
    res = db.read(query)
    return { "heroes": res }


@app.post("/fix")
async def i_know_better(body: Request):
    req = await body.json()
    return {
        "status" : "SUCCESS",
        "data" : req
    }


@app.delete("/delete/{name}")
def that_hero_sucks(name: str):
    db.delete(name)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("superheroes.main:app", host="0.0.0.0", port=8000, reload=True)
