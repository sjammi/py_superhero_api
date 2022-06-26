from typing import List, Union
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .db import Hero, HeroStats, HeroAffiliation


PydanticHero = sqlalchemy_to_pydantic(Hero)
PydanticStats = sqlalchemy_to_pydantic(HeroStats)
PydanticAffiliation = sqlalchemy_to_pydantic(HeroAffiliation)


class FullHero(BaseModel):
    info: PydanticHero
    stats: PydanticStats
    affiliations: List[str]


class HeroStatUpdate(BaseModel):
    alias: str
    HeroStats: PydanticStats


class HeroUpdate(BaseModel):
    response: Union[PydanticHero, HeroStatUpdate]
