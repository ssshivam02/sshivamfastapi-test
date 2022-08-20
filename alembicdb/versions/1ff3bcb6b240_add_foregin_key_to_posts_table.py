"""add foregin-key to posts table

Revision ID: 1ff3bcb6b240
Revises: b846e5ac02f5
Create Date: 2022-08-10 19:10:37.917932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ff3bcb6b240'
down_revision = 'b846e5ac02f5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable= False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", 
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')