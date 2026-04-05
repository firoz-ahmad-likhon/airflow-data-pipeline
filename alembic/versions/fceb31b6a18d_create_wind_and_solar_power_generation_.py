"""create wind_and_solar_power_generation table.

Revision ID: fceb31b6a18d
Revises: 3f7c61939b47
Create Date: 2026-04-05 09:01:41.084769

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fceb31b6a18d"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the table."""
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
    op.create_table(
        "wind_and_solar_power_generation",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("ingestion_ts", sa.TIMESTAMP()),
        sa.Column("window_from_utc", sa.TIMESTAMP()),
        sa.Column("window_to_utc", sa.TIMESTAMP()),
        sa.Column("request_url", sa.Text()),
        sa.Column("http_status", sa.Integer()),
        sa.Column("payload_json", sa.Text()),
        sa.Column("load_date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_wind_and_solar_power_generation_load_date",
        "wind_and_solar_power_generation",
        ["load_date"],
    )


def downgrade() -> None:
    """Drop the table."""
    op.drop_index(
        "ix_wind_and_solar_power_generation_load_date",
        table_name="wind_and_solar_power_generation",
    )
    op.drop_table("wind_and_solar_power_generation")
