"""NoteAccessOrm

Revision ID: 2a5b522d1c3c
Revises: 0418848d184b
Create Date: 2026-05-06 12:57:19.058196
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2a5b522d1c3c"
down_revision: Union[str, Sequence[str], None] = "0418848d184b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "NoteAccess",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("note_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["note_id"], ["Notes.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["Users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("NoteAccess")