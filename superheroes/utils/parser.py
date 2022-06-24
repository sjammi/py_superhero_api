import re
from typing import List, Dict, Union


class HeroParser:
    def parse_hero(self, raw_hero: Dict) -> Dict:
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

    def parse_hero_stats(self, raw_hero: Dict) -> Dict:
        return {
            "id": raw_hero["id"],
            "intelligence": 0,
            "strength": 0,
            "speed": 0,
            "durability": 0,
            "power": 0,
            "combat": 0,
        } | raw_hero.get("powerstats", {})

    def parse_hero_affiliations(self, raw_hero: Dict) -> List[Dict]:
        affiliations = raw_hero.get("connections", {"groupAffiliation": ""})[
            "groupAffiliation"
        ]
        return [
            {"id": raw_hero["id"], "affiliation": x}
            for x in re.split(
                ", |; ", affiliations  # affiliations can either be split by , or ;
            )
        ]

    def parse_raw_response(self, type: str, data: List[Dict]):
        """
        Parse incoming response from API into format expected for the requested tables.
        :param type - Assumes one of the following ["all", "hero", "stats", "affiliation"]
        :param data - raw data from the API
        """
        # TODO: tried using Literal from typing, but that needs a way to do validation without mypy or similar.
        if type not in ["all", "hero", "stats", "affiliation"]:
            raise Exception(
                "invalid table type given. Expects one of: [all, hero, stats, affiliation]"
            )

        def parse_single_hero(raw_hero: Dict, type: str) -> Union[Dict, List[Dict]]:
            if type == "all":
                return {
                    "hero": self.parse_hero(raw_hero),
                    "stats": self.parse_hero_stats(raw_hero),
                    "affiliation": self.parse_hero_affiliations(raw_hero),
                }
            elif type == "hero":
                return self.parse_hero(raw_hero)
            elif type == "stats":
                return self.parse_hero_stats(raw_hero)
            elif type == "affiliation":
                return self.parse_hero_affiliations(raw_hero)

        return [parse_single_hero(h, type) for h in data]

    def parse_db_response(self, hero: Dict) -> Dict:
        """
        Convert DB response to formatted Hero dict
        """
        return {
            "info": {
                "id": hero["id"],
                "name": hero["name"],
                "alias": hero["alias"],
                "species": hero["species"],
                "first_appearance": hero["first_appearance"],
                "publisher": hero["publisher"],
            },
            "stats": {
                "intelligence": hero["intelligence"],
                "strength": hero["strength"],
                "speed": hero["speed"],
                "durability": hero["durability"],
                "power": hero["power"],
                "combat": hero["combat"],
            },
            "affiliations": hero["affiliations"],
        }
