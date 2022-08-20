"""add content to posts table

Revision ID: 7a77f1e0d683
Revises: 55638432146f
Create Date: 2022-07-30 14:13:20.420525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a77f1e0d683'
down_revision = '55638432146f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts','content')
