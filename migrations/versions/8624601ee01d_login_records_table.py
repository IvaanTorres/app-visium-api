"""login records table

Revision ID: 8624601ee01d
Revises: 304c4f41b119
Create Date: 2023-08-24 18:37:54.586334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8624601ee01d'
down_revision: Union[str, None] = '304c4f41b119'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = '25388cdea768'


def upgrade() -> None:
    op.create_table(
        'login_records',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('nb_logins', sa.Integer, nullable=False, server_default="0"),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.func.now(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('login_records')
