"""Create files table

Revision ID: 1d4c13e656f3
Revises: abe4b3aaaf7f
Create Date: 2024-10-29 22:37:32.051083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d4c13e656f3'
down_revision: Union[str, None] = 'abe4b3aaaf7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
