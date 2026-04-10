from sqlalchemy import Column, DateTime, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class BmrsDataset(Base):
    """Raw BMRS dataset ingestion table."""

    __tablename__ = "bmrs_datasets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("gen_random_uuid()"),
    )
    ingestion_ts = Column(DateTime(timezone=True), nullable=True, index=True)
    window_from_utc = Column(DateTime(timezone=True), nullable=False)
    window_to_utc = Column(DateTime(timezone=True), nullable=False)
    data_type = Column(Text, nullable=True)
    request_url = Column(Text, nullable=True)
    http_status = Column(Integer, nullable=True)
    payload_json = Column(Text, nullable=True)
