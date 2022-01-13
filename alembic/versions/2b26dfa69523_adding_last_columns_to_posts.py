"""adding last columns to posts

Revision ID: 2b26dfa69523
Revises: 43007ee1ead9
Create Date: 2022-01-13 00:14:50.460801

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2b26dfa69523'
down_revision = '43007ee1ead9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published",
                  sa.Boolean(),
                  nullable=False,
                  server_default="TRUE"))
    op.add_column(
        "posts",
        sa.Column("created_at",
                  sa.TIMESTAMP(timezone=True),
                  nullable=False,
                  server_default=sa.text("NOW()")))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
