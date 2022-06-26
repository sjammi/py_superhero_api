import logging

import re
from typing import List, Dict, Union

from .api_models import *


class HeroParser:
    def parse_hero(self, raw_hero: ApiResponseHero) -> PydanticHero:
        bio = raw_hero.get(
            "biography", {"fullName": "", "firstAppearance": "", "publisher": ""}
        )
        return {
            "id": raw_hero["id"],
            "name": bio.get("fullName"),
            "alias": raw_hero.get("name"),
            "species": raw_hero.get("appearance", {"race": ""}).get("race"),
            "first_appearance": bio.get("firstAppearance"),
            "publisher": bio.get("publisher"),
        }

    def parse_hero_stats(self, raw_hero: ApiResponseHero) -> PydanticStats:
        return {
            "id": raw_hero["id"],
            "intelligence": 0,
            "strength": 0,
            "speed": 0,
            "durability": 0,
            "power": 0,
            "combat": 0,
        } | raw_hero.get("powerstats", {})

    def parse_hero_affiliations(
        self, raw_hero: ApiResponseHero
    ) -> List[PydanticAffiliation]:
        affiliations = raw_hero.get("connections", {"groupAffiliation": ""})[
            "groupAffiliation"
        ]
        return [
            {"id": raw_hero["id"], "affiliation": x}
            for x in re.split(
                ", |; ", affiliations  # affiliations can either be split by , or ;
            )
        ]

    def parse_raw_response(
        self, type: str, data: List[ApiResponseHero]
    ) -> List[FullHero]:
        """
        Parse incoming response from API into format expected for the requested tables.
        :param type - Assumes one of the following ["all", "hero", "stats", "affiliation"]
        :param data - raw data from the API
        :return List of heroes in FullHero format
        """
        # TODO: tried using Literal from typing, but that needs a way to do validation without mypy or similar.
        if type not in ["all", "hero", "stats", "affiliation"]:
            raise Exception(
                "invalid table type given. Expects one of: [all, hero, stats, affiliation]"
            )

        def parse_single_hero(
            raw_hero: ApiResponseHero, type: str
        ) -> List[Union[FullHero, PydanticHero, PydanticStats, PydanticAffiliation]]:
            if type == "all":
                return {
                    "hero": self.parse_hero(raw_hero),
                    "stats": self.parse_hero_stats(raw_hero),
                    "affiliations": self.parse_hero_affiliations(raw_hero),
                }
            elif type == "hero":
                return self.parse_hero(raw_hero)
            elif type == "stats":
                return self.parse_hero_stats(raw_hero)
            elif type == "affiliation":
                return self.parse_hero_affiliations(raw_hero)

        return [parse_single_hero(h, type) for h in data]

    def parse_db_response(self, hero: Dict) -> FullHero:
        """
        Convert DB response to formatted Hero
        """
        return {
            "hero": {
                "id": hero["id"],
                "name": hero["name"],
                "alias": hero["alias"],
                "species": hero["species"],
                "first_appearance": hero["first_appearance"],
                "publisher": hero["publisher"],
            },
            "stats": {
                "id": hero["id"],
                "intelligence": hero["intelligence"],
                "strength": hero["strength"],
                "speed": hero["speed"],
                "durability": hero["durability"],
                "power": hero["power"],
                "combat": hero["combat"],
            },
            "affiliations": hero["affiliations"],
        }
