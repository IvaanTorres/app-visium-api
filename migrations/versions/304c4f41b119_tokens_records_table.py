"""tokens records table

Revision ID: 304c4f41b119
Revises: 25388cdea768
Create Date: 2023-08-24 18:37:11.315024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '304c4f41b119'
down_revision: Union[str, None] = '25388cdea768'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = '25388cdea768'


def upgrade() -> None:
    op.create_table(
        'tokens_records',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('token', sa.String(50), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('tokens_records')
