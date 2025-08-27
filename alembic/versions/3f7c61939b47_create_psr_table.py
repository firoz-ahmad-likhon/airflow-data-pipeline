"""create psr table.

Revision ID: 3f7c61939b47
Revises: adb3d9d72bb2
Create Date: 2025-08-27 18:22:38.742504

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3f7c61939b47"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the psr table."""
    op.create_table(
        "psr",
        sa.Column("curve_name", sa.String(length=255), primary_key=True),
        sa.Column(
            "curve_date",
            sa.DateTime(timezone=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("value", sa.Numeric()),
        sa.PrimaryKeyConstraint("curve_name", "curve_date"),
        comment="Power generation data for different curves over time.",
    )

    # Add column comments
    op.execute(
        "COMMENT ON COLUMN psr.curve_name IS 'The name of the curve, representing the type of power generation (e.g., solar, wind).';",
    )
    op.execute(
        "COMMENT ON COLUMN psr.curve_date IS 'Timestamp indicating the start_date, stored in UTC.';",
    )
    op.execute(
        "COMMENT ON COLUMN psr.value IS 'The measured value associated with the curve at the specified date and time.';",
    )


def downgrade() -> None:
    """Drop the psr table."""
    op.drop_table("psr")
