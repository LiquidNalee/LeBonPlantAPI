import pytest
from fastapi.testclient import TestClient
from pycircuitbreaker import CircuitBreaker, CircuitBreakerState
from pydantic import ValidationError
from pytest_mock import MockerFixture

from instance import settings
from lebonplantapi.controllers.api.schemas import ReadyResponseModel


class TestPing:
    def test_no_cache(self, client: TestClient) -> None:
        ret = client.get("/lebonplantapi/liveness")
        assert ret.headers["Cache-Control"] == "no-cache"

    def test_response(self, client: TestClient) -> None:
        ret = client.get("/lebonplantapi/liveness")

        assert ret.status_code == 200
        assert ret.json() == {"app": "ok"}


class TestReady:
    cb_ids = list(ReadyResponseModel.__fields__)

    def test_no_cache(self, client: TestClient) -> None:
        ret = client.get("/lebonplantapi/readiness")
        assert ret.headers["Cache-Control"] == "no-cache"

    def test_response__db_ok(self, client: TestClient) -> None:
        ret = client.get("/lebonplantapi/readiness")
        content = ret.json()

        assert ret.status_code == 200
        assert len(content) == len(self.cb_ids)
        for cb_id in self.cb_ids:
            assert content[cb_id] == "closed"

    def test_response__db_ko(self, client: TestClient, mocker: MockerFixture) -> None:
        test_cbreakers = [CircuitBreaker(breaker_id=cb_id) for cb_id in self.cb_ids]
        test_cbreakers[0]._strategy._state = CircuitBreakerState.OPEN
        patched = mocker.patch(
            "lebonplantapi.controllers.health.circuit_breaker_registry"
        )
        patched.get_open_circuits.return_value = test_cbreakers
        patched.get_circuits.return_value = test_cbreakers

        ret = client.get("/lebonplantapi/readiness")
        content = ret.json()

        assert ret.status_code == 500
        assert len(content) == len(self.cb_ids)
        assert content[self.cb_ids[0]] == "open"
        for i in range(1, len(self.cb_ids)):
            assert content[self.cb_ids[i]] == "closed"

    def test_response__missing_breakers(
        self, client: TestClient, mocker: MockerFixture
    ) -> None:
        patched = mocker.patch(
            "lebonplantapi.controllers.health.circuit_breaker_registry"
        )
        patched.get_open_circuits.return_value = []
        patched.get_circuits.return_value = []

        with pytest.raises(ValidationError):
            client.get("/lebonplantapi/readiness")


class TestVersion:
    def test_version__valid(self, client: TestClient) -> None:
        old_version = settings.application_version
        settings.application_version = "abcdef12"
        try:
            ret = client.get("/lebonplantapi/version")

            assert ret.status_code == 200
            assert ret.json() == {"version": "abcdef12"}
        finally:
            settings.application_version = old_version

    def test_version__invalid(self, client: TestClient) -> None:
        old_version = settings.application_version
        settings.application_version = ""
        try:
            ret = client.get("/lebonplantapi/version")

            assert ret.status_code == 404
        finally:
            settings.application_version = old_version
