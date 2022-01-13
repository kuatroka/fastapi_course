"""add content column to posts

Revision ID: b7d8299788cd
Revises: a33bdc769db2
Create Date: 2022-01-12 23:32:57.822439

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b7d8299788cd'
down_revision = 'a33bdc769db2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
