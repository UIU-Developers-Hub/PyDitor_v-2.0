"""Add files table

Revision ID: e9daca2e3b63
Revises: e1f3a5bdb062
Create Date: 2024-10-30 06:29:01.432161

"""
from typing import Sequence, Union


from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9daca2e3b63'
down_revision = 'e1f3a5bdb062'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'files',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('path', sa.String, nullable=False),
        sa.Column('content', sa.Text, nullable=True),
        sa.Column('file_type', sa.String, default="file"),
        sa.Column('is_directory', sa.Boolean, default=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now())
    )




def downgrade() -> None:
    # Drop the 'files' table if downgrading
    op.drop_table('files')