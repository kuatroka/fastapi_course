"""add user table

Revision ID: f85628f9258a
Revises: b7d8299788cd
Create Date: 2022-01-12 23:40:25.737149

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f85628f9258a'
down_revision = 'b7d8299788cd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users", sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at",
                  sa.TIMESTAMP(timezone=True),
                  nullable=False,
                  server_default=sa.func.now()), sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"))
    pass


def downgrade():
    op.drop_table("users")
    pass
