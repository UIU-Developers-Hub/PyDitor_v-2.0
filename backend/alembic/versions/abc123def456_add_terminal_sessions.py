# backend/alembic/versions/abc123def456_add_terminal_sessions.py

"""Add terminal sessions table

Revision ID: abc123def456
Revises: 4b0d964c5091  # Points to the previous migration's revision ID
Create Date: 2024-02-07
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'abc123def456'
down_revision = '4b0d964c5091'  # This points to the previous migration
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'terminal_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('terminal_id', sa.String(), nullable=False),
        sa.Column('history', sa.Text(), nullable=True),
        sa.Column('current_directory', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('terminal_id')
    )

def downgrade():
    op.drop_table('terminal_sessions')
