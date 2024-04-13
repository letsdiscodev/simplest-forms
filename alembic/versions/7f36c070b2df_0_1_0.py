"""0.1.0

Revision ID: 7f36c070b2df
Revises:
Create Date: 2024-04-13 03:07:57.110460

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7f36c070b2df"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "form_submissions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("client_addr", sa.String(), nullable=False),
        sa.Column("form", sa.String(), nullable=False),
        sa.Column("content", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_form_submissions")),
    )
    op.create_index(
        op.f("ix_form_submissions_client_addr"),
        "form_submissions",
        ["client_addr"],
        unique=False,
    )
    op.create_index(
        op.f("ix_form_submissions_created"),
        "form_submissions",
        ["created"],
        unique=False,
    )
    op.create_index(
        op.f("ix_form_submissions_form"), "form_submissions", ["form"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_form_submissions_form"), table_name="form_submissions")
    op.drop_index(op.f("ix_form_submissions_created"), table_name="form_submissions")
    op.drop_index(
        op.f("ix_form_submissions_client_addr"), table_name="form_submissions"
    )
    op.drop_table("form_submissions")
