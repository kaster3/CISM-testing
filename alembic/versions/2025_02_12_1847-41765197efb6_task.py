"""task

Revision ID: 41765197efb6
Revises: 
Create Date: 2025-02-12 18:47:50.186657

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "41765197efb6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "NEW",
                "IN_PROGRESS",
                "COMPLETED",
                "ERROR",
                name="taskstatusenum",
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tasks")),
    )


def downgrade() -> None:
    op.drop_table("tasks")
