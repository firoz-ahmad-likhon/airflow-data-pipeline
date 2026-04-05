"""create wind_and_solar_power_generation table.

Revision ID: fceb31b6a18d
Revises: 3f7c61939b47
Create Date: 2026-04-05 09:01:41.084769

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fceb31b6a18d"
down_revision: str | Sequence[str] | None = "3f7c61939b47"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the table."""
    op.create_table(
        "wind_and_solar_power_generation",
        sa.Column("ingestion_ts", sa.TIMESTAMP()),
        sa.Column("window_from_utc", sa.TIMESTAMP()),
        sa.Column("window_to_utc", sa.TIMESTAMP()),
        sa.Column("request_url", sa.Text()),
        sa.Column("http_status", sa.Integer()),
        sa.Column("payload_json", sa.Text()),
        sa.Column("load_date", sa.Date()),
        postgresql_partition_by="RANGE (load_date)",
    )


def downgrade() -> None:
    """Drop the table."""
    op.drop_table("wind_and_solar_power_generation")
