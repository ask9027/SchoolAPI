"""Add User and Post Tables

Revision ID: 43ae4494a6eb
Revises: 
Create Date: 2022-12-31 21:24:38.223340

"""
import sqlalchemy as sa
from sqlalchemy.sql import text

from alembic import op

# revision identifiers, used by Alembic.
revision = "43ae4494a6eb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "uid",
            sa.String(),
            nullable=False,
            primary_key=True,
            server_default=text("REPLACE(gen_random_uuid()::text,'-','')"),
        ),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
    )
    op.create_table(
        "students",
        sa.Column(
            "uid",
            sa.String(),
            nullable=False,
            primary_key=True,
            server_default=text("REPLACE(gen_random_uuid()::text,'-','')"),
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("className", sa.String(), nullable=False),
        sa.Column("rollNumber", sa.Integer(), nullable=False, unique=True),
    )
    op.create_table(
        "tokenblacklist",
        sa.Column("_id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("token", sa.String(), nullable=False, unique=True),
        sa.Column("email", sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("students")
    op.drop_table("tokenblacklist")
    pass
