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


@app.post("/fix")
async def i_know_better(body: Request):
    return {
        "status" : "SUCCESS",
        "data" : await body.json()
    }


@app.delete("/delete/{name}")
def that_hero_sucks(name: str):
    db.delete(name)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("superheroes.main:app", host="0.0.0.0", port=8000, reload=True)
