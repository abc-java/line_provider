"""empty message

Revision ID: 1387284802e5
Revises: 
Create Date: 2025-02-05 02:29:56.064081

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1387284802e5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("coefficient", sa.Numeric(), nullable=False),
        sa.Column("deadline", sa.Integer(), nullable=False),
        sa.Column(
            "state",
            sa.Enum("NEW", "FINISHED_WIN", "FINISHED_LOSE", name="eventstate"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("events")
    # ### end Alembic commands ###
