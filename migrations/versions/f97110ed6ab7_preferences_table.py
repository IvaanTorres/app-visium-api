"""preferences table

Revision ID: f97110ed6ab7
Revises: 8624601ee01d
Create Date: 2023-08-24 18:38:15.294874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f97110ed6ab7'
down_revision: Union[str, None] = '8624601ee01d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = '25388cdea768'


def upgrade() -> None:
    op.create_table(
        'preferences',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('locale', sa.String(50), nullable=False, server_default="'en'"),
        sa.Column('welcomeMsgSize', sa.Integer, nullable=False, server_default="30"),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('preferences')
