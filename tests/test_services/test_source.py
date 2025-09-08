from http import HTTPStatus
from typing import Any
import pytest
import pendulum
from dags.services.source import SourceAPI


class TestSourceAPI:
    """Test class for SourceAPI."""

    def test_url_friendly_datetime(self) -> None:
        """Test that datetime is correctly formatted for the API URL."""
        assert (
            SourceAPI().url_friendly_datetime(pendulum.datetime(2024, 10, 16, 14, 30))
            == "2024-10-16%2014%3A30"
        )

    def test_fetch_json(
        self,
        monkeypatch: pytest.MonkeyPatch,
        mock_data: dict[str, list[dict[str, Any]]],
    ) -> None:
        """Test the API data fetching functionality with mocked response.

        :param mock_data: Mocked data from fixture.
        """

        class MockResponse:
            """The best approach to mocking is to mock the object where it is used, not where it is defined."""

            status_code = HTTPStatus.OK

            def json(self) -> dict[str, list[dict[str, Any]]]:
                return mock_data

        def mock_get(url: str) -> MockResponse:
            """Mock function for requests.get(url)."""
            return MockResponse()

        from_date = pendulum.datetime(2024, 10, 10)
        to_date = pendulum.datetime(2024, 10, 12)

        # Monkeypatch the invoke method to return the mocked response
        monkeypatch.setattr("dags.services.source.requests.get", mock_get)

        # Call the method that fetches the JSON
        result = SourceAPI().fetch_json(from_date, to_date)

        assert isinstance(result, dict)
        assert result["data"][0]["psrType"] == "Wind Onshore"
        assert result["data"][1]["psrType"] == "Wind Offshore"
