"""rmover admin

Revision ID: df4d81f4f43d
Revises: 583169a46551
Create Date: 2025-07-06 15:37:44.070313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df4d81f4f43d'
down_revision: Union[str, Sequence[str], None] = '583169a46551'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuarios', 'admin')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuarios', sa.Column('admin', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###
