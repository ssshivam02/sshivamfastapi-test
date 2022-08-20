"""add last few columns to posts table

Revision ID: 475b38d1364f
Revises: 1ff3bcb6b240
Create Date: 2022-08-10 19:42:24.360569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '475b38d1364f'
down_revision = '1ff3bcb6b240'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')