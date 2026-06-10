"""Set notes.folder_id to NULL when a folder is deleted.

Revision ID: 64b5bd901eaf
Revises: 2a5b522d1c3c
"""

from typing import Sequence, Union

from alembic import op


revision: str = "64b5bd901eaf"
down_revision: Union[str, Sequence[str], None] = "2a5b522d1c3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "Notes_folder_id_fkey",
        "Notes",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "Notes_folder_id_fkey",
        "Notes",
        "Folders",
        ["folder_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "Notes_folder_id_fkey",
        "Notes",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "Notes_folder_id_fkey",
        "Notes",
        "Folders",
        ["folder_id"],
        ["id"],
    )