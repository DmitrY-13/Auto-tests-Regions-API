from typing import Any

import requests

from settings import settings


class ApiClient:
    GET_REGIONS = '/1.0/regions'

    def __init__(self, session: requests.Session):
        self._session = session

    def get_regions(
        self,
        q: str | Any = None,
        country_code: str | Any = None,
        page: int | Any = None,
        page_size: int | Any = None,
    ) -> requests.Response:
        """
        :param q: Arbitrary string for fuzzy search by region name
        :param country_code: Country code for filtering
        :param page: Sequential number of page
        :param page_size: Number of items per page
        :return: requests.Response
        """

        return self._session.get(
            settings.host + self.GET_REGIONS,
            params={
                'q': q,
                'country_code': country_code,
                'page': page,
                'page_size': page_size,
            },
        )
