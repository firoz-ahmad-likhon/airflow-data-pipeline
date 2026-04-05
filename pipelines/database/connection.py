from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from pipelines.utils.db_helper import DBHelper

DATABASE_URL = DBHelper.database_url()

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_session() -> Session:
    """Get a new SQLAlchemy session."""
    return SessionLocal()
