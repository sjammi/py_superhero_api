import logging
from requests import get
from typing import List

from .api_models import ApiResponseHero

API_URL = "https://akabab.github.io/superhero-api/api"
API_ENDPOINTS = {"all": "/all.json", "id": "/id"}


class APIHandler:
    """
    A class for handling requests and responses from the superheroes API.
    """

    def __init__(self):
        self.url = API_URL

    def query_api(self, endpoint="all", id=None) -> List[ApiResponseHero]:
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
