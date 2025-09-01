import pytest
from dags.utils.db_helper import DBHelper


class TestDBHelper:
    """Test class for DBHelper."""

    def test_database_url_valid(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test database_url builds a valid connection string."""
        monkeypatch.setenv("POSTGRES_USER", "test_user")
        monkeypatch.setenv("POSTGRES_PASSWORD", "test_pass")
        monkeypatch.setenv("POSTGRES_HOST", "localhost")
        monkeypatch.setenv("POSTGRES_PORT", "6543")
        monkeypatch.setenv("POSTGRES_DB", "test_db")

        assert (
            DBHelper.database_url()
            == "postgresql+psycopg2://test_user:test_pass@localhost:6543/test_db"
        )

    def test_database_url_defaults_port(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test database_url uses default port 5432 when not set."""
        monkeypatch.setenv("POSTGRES_USER", "user")
        monkeypatch.setenv("POSTGRES_PASSWORD", "pass")
        monkeypatch.setenv("POSTGRES_HOST", "db")
        monkeypatch.delenv("POSTGRES_PORT", raising=False)  # unset port
        monkeypatch.setenv("POSTGRES_DB", "mydb")

        assert (
            DBHelper.database_url("postgresql") == "postgresql://user:pass@db:5432/mydb"
        )

    def test_database_url_missing_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test database_url raises error when required env vars missing."""
        monkeypatch.delenv("POSTGRES_USER", raising=False)
        monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)
        monkeypatch.delenv("POSTGRES_HOST", raising=False)
        monkeypatch.delenv("POSTGRES_DB", raising=False)

        with pytest.raises(
            ValueError,
            match="POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, and POSTGRES_DB must be set",
        ):
            DBHelper.database_url()
