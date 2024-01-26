"""Cria tabela de contas a pagar e receber

Revision ID: 043a2613be3b
Revises: 
Create Date: 2024-01-25 12:17:45.732761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '043a2613be3b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('contas_a_pagar_receber',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('descricao', sa.String(length=30), nullable=True),
    sa.Column('valor', sa.Numeric(), nullable=True),
    sa.Column('tipo', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('contas_a_pagar_receber')
