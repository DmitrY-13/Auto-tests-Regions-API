import logging

import pytest
import requests

from api.client import ApiClient

logger = logging.getLogger(__name__)


@pytest.fixture
def session() -> requests.Session:
    def log_response(r, *args, **kwargs):
        logger.info(f'Request: {r.request.method} {r.request.url}')
        logger.info(f'Response: {r.status_code} {r.text}')
        return r

    session = requests.Session()
    session.hooks['response'].append(log_response)

    return session


@pytest.fixture
def client(session: requests.Session) -> ApiClient:
    return ApiClient(session)
