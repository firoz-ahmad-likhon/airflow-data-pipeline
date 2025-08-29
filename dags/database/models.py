from sqlalchemy import Column, String, DateTime, Numeric
from sqlalchemy.orm import declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class PSR(Base):
    """PSR table."""

    __tablename__ = "psr"

    curve_name = Column(String(255), primary_key=True)
    curve_date = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    value = Column(Numeric(), nullable=True)
