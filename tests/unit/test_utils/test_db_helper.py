import pytest
from dags.utils.db_helper import DBHelper


class TestDBHelper:
    """Test class for DBHelper."""

    @pytest.mark.parametrize(
        ("env_vars", "driver", "expected_url"),
        [
            (
                {
                    "POSTGRES_USER": "test_user",
                    "POSTGRES_PASSWORD": "test_pass",
                    "POSTGRES_HOST": "localhost",
                    "POSTGRES_PORT": "6543",
                    "POSTGRES_DB": "test_db",
                },
                None,
                "postgresql+psycopg2://test_user:test_pass@localhost:6543/test_db",
            ),
            (
                {
                    "POSTGRES_USER": "user",
                    "POSTGRES_PASSWORD": "pass",
                    "POSTGRES_HOST": "db",
                    "POSTGRES_DB": "mydb",
                },
                "postgresql",
                "postgresql://user:pass@db:5432/mydb",
            ),
        ],
    )
    def test_database_url(
        self,
        monkeypatch: pytest.MonkeyPatch,
        env_vars: dict[str, str],
        driver: str | None,
        expected_url: str,
    ) -> None:
        """Test database_url builds a valid connection string for various scenarios."""
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        # Ensure port is unset if not in the test case's env vars
        if "POSTGRES_PORT" not in env_vars:
            monkeypatch.delenv("POSTGRES_PORT", raising=False)

        url = DBHelper.database_url(driver) if driver else DBHelper.database_url()
        assert url == expected_url

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
