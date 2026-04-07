from http import HTTPStatus
from typing import Any

import pendulum
import pytest
from pipelines.services.wind_solar_api import WindSolarAPI


class TestWindSolarAPI:
    """Test class for WindSolarAPI."""

    def test_url_friendly_datetime(self) -> None:
        """Test that datetime is correctly formatted for the API URL."""
        assert WindSolarAPI().url_friendly_datetime(pendulum.datetime(2024, 10, 16, 14, 30)) == "2024-10-16%2014%3A30"

    def test_fetch_json(
        self,
        monkeypatch: pytest.MonkeyPatch,
        mock_data: dict[str, list[dict[str, Any]]],
    ) -> None:
        """Test the API data fetching functionality with mocked response.

        :param mock_data: Mocked data from fixture.
        """

        class MockResponse:
            """Mock response."""

            status_code = HTTPStatus.OK

            def json(self) -> dict[str, list[dict[str, Any]]]:
                return mock_data

        def mock_get(url: str) -> MockResponse:
            """Mock function for requests.get(url)."""
            return MockResponse()

        from_date = pendulum.datetime(2024, 10, 10)
        to_date = pendulum.datetime(2024, 10, 12)

        # Monkeypatch the get method to return the mocked response
        monkeypatch.setattr("pipelines.services.wind_solar_api.requests.get", mock_get)

        # Call the method that fetches the JSON
        result = WindSolarAPI().fetch_json(from_date, to_date)

        assert isinstance(result, dict)
        assert result["window_from_utc"] == from_date.to_iso8601_string()
        assert result["window_to_utc"] == to_date.to_iso8601_string()
        assert result["http_status"] == HTTPStatus.OK
        assert "wind-and-solar" in result["request_url"]
        assert '"psrType": "Wind Onshore"' in result["payload_json"]
