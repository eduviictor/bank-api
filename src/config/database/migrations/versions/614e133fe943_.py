"""empty message

Revision ID: 614e133fe943
Revises:
Create Date: 2025-02-15 01:15:49.681475

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '614e133fe943'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment_account',
    sa.Column('balance', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('OPEN', 'CLOSED', 'BLOCKED', name='payment_account_status_enum'), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('institution_code', sa.String(length=255), nullable=False),
    sa.Column('branch_code', sa.String(length=255), nullable=False),
    sa.Column('account_code', sa.String(length=255), nullable=False),
    sa.Column('account_type', sa.Enum('CHECKING', 'SAVINGS', name='payment_account_type_enum'), nullable=False),
    sa.Column('tax_id', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment_account')
    op.execute('DROP TYPE payment_account_status_enum')
    op.execute('DROP TYPE payment_account_type_enum')
    # ### end Alembic commands ###
