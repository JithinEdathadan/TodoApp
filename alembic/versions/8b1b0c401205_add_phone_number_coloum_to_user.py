"""Add phone_number column to user

Revision ID: 8b1b0c401205
Revises: 
Create Date: 2025-05-02 14:53:25.237219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b1b0c401205'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable=True))

def downgrade() -> None:
    op.drop_column('users','phone_number')
