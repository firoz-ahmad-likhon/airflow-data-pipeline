import logging
import os
import psycopg2
from psycopg2 import extras
from psycopg2.extensions import connection
from collections.abc import Sequence
from typing import Any, cast


class PostgresSQL:
    """The class is responsible for database connection and operations."""

    def __init__(self) -> None:
        """Initialize PostgresSQL class."""
        self.conn_config = self._get_conn_config()

    def _get_conn_config(self) -> dict[str, Any]:
        """Get DB config from environment variables."""
        dsn = os.getenv("POSTGRES_CONNECTION_STRING")
        if dsn:
            return {"dsn": dsn}
        return {
            "host": os.getenv("POSTGRES_HOST"),
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "port": int(os.getenv("POSTGRES_PORT", "5432")),
        }

    def _get_connection(self) -> connection:
        """Establish and return a new connection."""
        try:
            return psycopg2.connect(**self.conn_config)
        except psycopg2.Error as e:
            logging.error("Error connecting to the database: %s", str(e))
            raise

    def query(self, query: str, params: Sequence[Any] | None = None) -> None:
        """Execute a query without return."""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
        except Exception as e:
            logging.error("Query execution failed: %s\nError: %s", query, e)
            raise

    def bulk_insert(self, query: str, data: Sequence[tuple[Any, ...]]) -> None:
        """Run a batch insert."""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                extras.execute_values(cursor, query, data)

    def fetch(
        self,
        query: str,
        params: Sequence[Any] | None = None,
    ) -> list[tuple[Any, ...]]:
        """Fetch all rows from a query."""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cast(list[tuple[Any, ...]], cursor.fetchall())

    def single(
        self,
        query: str,
        params: Sequence[Any] | None = None,
    ) -> tuple[Any, ...] | None:
        """Fetch a single row from a query."""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cast(tuple[Any, ...] | None, cursor.fetchone())
