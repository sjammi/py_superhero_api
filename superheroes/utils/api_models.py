from typing import List, Union
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .db import Hero, HeroStats, HeroAffiliation


PydanticHero = sqlalchemy_to_pydantic(Hero)
PydanticStats = sqlalchemy_to_pydantic(HeroStats)
PydanticAffiliation = sqlalchemy_to_pydantic(HeroAffiliation)


class FullHero(BaseModel):
    hero: PydanticHero
    stats: PydanticStats
    affiliations: List[Union[str, PydanticAffiliation]]


class HeroStatUpdate(BaseModel):
    alias: str
    HeroStats: PydanticStats


class HeroUpdate(BaseModel):
    response: Union[PydanticHero, HeroStatUpdate]


### API Response models ###
# I'd prefer nested object types in Typescript style, but that isn't supported here?


class ApiResponseAppearance(BaseModel):
    race: str
    # includes other unused values


class ApiResponseBiography(BaseModel):
    fullName: str
    firstAppearance: str
    publisher: str
    # includes other unused values


class ApiResponseConnections(BaseModel):
    groupAffiliation: str


class ApiResponseHero(BaseModel):
    id: str
    name: str
    powerstats: PydanticStats
    appearance: ApiResponseAppearance
    biography: ApiResponseBiography
    connections: ApiResponseConnections
