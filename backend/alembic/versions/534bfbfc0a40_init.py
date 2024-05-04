"""init

Revision ID: 534bfbfc0a40
Revises: 
Create Date: 2024-05-01 01:34:54.452841

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '534bfbfc0a40'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sheets',
        sa.Column('id', sa.Integer, primary_key=True)
    )

    op.create_table(
        'columns',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('sheet_id', sa.Integer, sa.ForeignKey("sheets.id"), nullable=False),
    )

    op.create_table(
        'cells',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('row_index', sa.Integer, nullable=False),
        sa.Column('value', sa.String, nullable=False),
        sa.Column('column_id', sa.Integer, sa.ForeignKey("columns.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('cells')
    op.drop_table('columns')
    op.drop_table('sheets')
