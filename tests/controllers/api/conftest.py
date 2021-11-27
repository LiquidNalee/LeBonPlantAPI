from asyncio import AbstractEventLoop
from typing import Generator
from urllib.parse import urlparse

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from instance import settings
from lebonplantapi import create_app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """Session-wide test `FastAPI` application."""
    app = create_app()
    sqlalchemy_database_uri = settings.sqlalchemy_database_uri
    if sqlalchemy_database_uri:
        sqlalchemy_database_uri_parsed = urlparse(sqlalchemy_database_uri)
        if "test" not in sqlalchemy_database_uri_parsed.path:
            pytest.exit("There is a risk, tests can't continue")
    return app


@pytest.fixture(scope="session")
def client(
    app: FastAPI, event_loop: AbstractEventLoop
) -> Generator[TestClient, None, None]:
    """Return a FastAPI test client.

    An instance of :class:`fastapi.test_client.TestClient` by default.
    """
    with TestClient(app) as client:
        yield client
