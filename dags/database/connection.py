from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dags.utils.db_helper import DBHelper


class DBConnection:
    """Wrapper for SQLAlchemy engine and sessions."""

    def __init__(
        self,
        driver: str = "postgresql+psycopg2",
        echo: bool = False,
        autoflush: bool = False,
        autocommit: bool = False,
    ):
        """Initialize."""
        self.driver = driver
        self.echo = echo
        self.autoflush = autoflush
        self.autocommit = autocommit

        # Build URL using DBHelper
        self.database_url = DBHelper.database_url(driver=self.driver)

        # Create engine
        self.engine = create_engine(self.database_url, echo=self.echo, future=True)

        # Session factory
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=self.autoflush,
            autocommit=self.autocommit,
        )

    def get_session(self) -> Session:
        """Get a new SQLAlchemy session (context manager style)."""
        return self.SessionLocal()
