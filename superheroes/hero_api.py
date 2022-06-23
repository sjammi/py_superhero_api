import logging
import re
from requests import get
from typing import List, Dict, Union

API_URL = "https://akabab.github.io/superhero-api/api"
API_ENDPOINTS = {"all": "/all.json", "id": "/id"}


class HeroParser:
    def parse_hero(self, raw_hero: Dict) -> Dict:
        bio = raw_hero.get(
            "biography", {"fullName": "", "firstAppearance": "", "Publisher": ""}
        )
        return {
            "id": raw_hero["id"],
            "name": bio.get("fullName"),
            "alias": raw_hero.get("name"),
            "species": raw_hero.get("appearance", {"race": ""}).get("race"),
            "first_appearance": bio.get("firstAppearance"),
            "publisher": bio.get("Publisher"),
        }

    def parse_hero_stats(self, raw_hero: Dict) -> Dict:
        return {
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
                ", |; ", affiliations
            )  # affiliations can either be split by , or ;
        ]

    def parse_raw_response(self, type: str, data: List[Dict]):
        """
        Parse incoming response from API into format expected for the requested tables.
        :param table - Assumes one of the following ["all", "hero", "stats", "affiliation"]
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


class APIHandler:
    """
    A class for handling requests and responses from the superheroes API.
    """

    def __init__(self):
        self.url = API_URL

    def query_api(self, endpoint="all", id=None) -> List[Dict]:
        """
        Handles the GET request to the API.
        :param endpoint - assumes one of the endpoints specified in API_ENDPOINTS. Will throw an error otherwise.
        :return raw response as list
        """
        if endpoint not in API_ENDPOINTS.keys():
            raise Exception(
                f"Invalid endpoint specified. Please use one of the following: {API_ENDPOINTS.keys()}"
            )

        query_url = self.url + API_ENDPOINTS[endpoint]
        if id and endpoint != "all":
            query_url += f"/{id}.json"

        logging.info(f"Querying endpoint: {query_url}")
        res = get(query_url)
        hero_data = res.json()
        return hero_data if isinstance(hero_data, list) else [hero_data]
