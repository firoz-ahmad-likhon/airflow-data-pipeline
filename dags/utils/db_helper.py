import os


class DBHelper:
    """Helper class for utils related to databases."""

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
