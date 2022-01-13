"""add foreign-key to posts table

Revision ID: 43007ee1ead9
Revises: f85628f9258a
Create Date: 2022-01-13 00:05:38.486613

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '43007ee1ead9'
down_revision = 'f85628f9258a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk",
                          source_table="posts",
                          referent_table="users",
                          local_cols=["owner_id"],
                          remote_cols=["id"],
                          ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
