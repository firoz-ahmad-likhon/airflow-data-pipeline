from sqlalchemy import Column, Date, DateTime, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class WindAndSolarPowerGeneration(Base):
    """Wind and solar power generation ingestion table."""

    __tablename__ = "wind_and_solar_power_generation"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("gen_random_uuid()"),
    )
    ingestion_ts = Column(DateTime(timezone=True), nullable=True)
    window_from_utc = Column(DateTime(timezone=True), nullable=False)
    window_to_utc = Column(DateTime(timezone=True), nullable=False)
    request_url = Column(Text, nullable=True)
    http_status = Column(Integer, nullable=True)
    payload_json = Column(Text, nullable=True)
    load_date = Column(Date, nullable=False)
