import http
import json
from typing import Any
from urllib.parse import quote

import pendulum
import requests  # type: ignore


class WindSolarAPI:
    """Read wind and solar generation data from the external API."""

    API_URL = "https://data.elexon.co.uk/bmrs/api/v1/generation/actual/per-type/wind-and-solar?from={from_date}&to={to_date}&format=json"

    def url_friendly_datetime(self, dt: pendulum.DateTime) -> str:
        """To format datetime object for API query.

        :param dt: datetime object
        :return:
        """
        return quote(dt.strftime("%Y-%m-%d %H:%M"))

    def fetch_json(
        self,
        from_date: pendulum.DateTime,
        to_date: pendulum.DateTime,
    ) -> dict[str, Any]:
        """Fetch JSON data from API.

        :param from_date:   from start date in datetime format
        :param to_date:     to start date in datetime format
        :return:            JSON data as a dictionary
        """
        url = WindSolarAPI.API_URL.format(
            from_date=self.url_friendly_datetime(from_date),
            to_date=self.url_friendly_datetime(to_date),
        )

        response = requests.get(url)
        payload = response.json()

        if response.status_code != http.HTTPStatus.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return {
            "ingestion_ts": pendulum.now(tz="UTC").to_iso8601_string(),
            "window_from_utc": from_date.to_iso8601_string(),
            "window_to_utc": to_date.to_iso8601_string(),
            "request_url": url,
            "http_status": response.status_code,
            "payload_json": json.dumps(payload),
            "load_date": pendulum.now(tz="UTC").to_date_string(),
        }
