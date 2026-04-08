import os
from datetime import datetime

import pendulum


class Helper:
    """Helper class to prepare acquisition of data from the API and handle the API data."""

    @staticmethod
    def date_param(dt: datetime) -> pendulum.DateTime:
        """Get the start datetime for data collection.

        :param dt: datetime to be converted to nearest 30 minutes
        :return: datetime
        """
        dt = pendulum.instance(dt)

        # API published data is 90 minutes behind
        return Helper.floor_to_30_min(dt).subtract(minutes=90)

    @staticmethod
    def floor_to_30_min(dt: pendulum.DateTime) -> pendulum.DateTime:
        """Floor the given datetime to the nearest 30 minutes.

        :param dt: datetime to be floored
        :return: floored datetime
        """
        return dt.replace(minute=(dt.minute // 30) * 30, second=0, microsecond=0)

    @staticmethod
    def database_url(driver: str = "postgresql+psycopg2") -> str:
        """Build the connection url.

        :param driver: Driver name of a database
        :return: A connection url
        """
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB")

        if not all([user, password, host, db]):
            raise ValueError(
                "POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, and POSTGRES_DB must be set",
            )

        return f"{driver}://{user}:{password}@{host}:{port}/{db}"
