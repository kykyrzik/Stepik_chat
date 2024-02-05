"""test

Revision ID: fab4dcce52eb
Revises: 
Create Date: 2024-02-04 01:58:42.389387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fab4dcce52eb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('media', sa.Column('name', sa.String(), nullable=False))
    op.add_column('media', sa.Column('url', sa.String(), nullable=False))
    op.create_index(op.f('ix_media_name'), 'media', ['name'], unique=False)
    op.create_unique_constraint(None, 'media', ['url'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'media', type_='unique')
    op.drop_index(op.f('ix_media_name'), table_name='media')
    op.drop_column('media', 'url')
    op.drop_column('media', 'name')
    # ### end Alembic commands ###