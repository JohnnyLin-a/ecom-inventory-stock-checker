"""create main tables

Revision ID: 6e8567af4db5
Revises: 
Create Date: 2022-01-17 22:30:17.297558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e8567af4db5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ecoms',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('website', sa.String(50), nullable=False, unique=True),
    )
    op.create_table(
        'executions',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('ecom_id', sa.BigInteger, sa.ForeignKey('ecoms.id'), nullable=False),
        sa.Column('exec_datetime', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    op.create_table(
        'categories',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
    )
    op.create_table(
        'items',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('ecom_id', sa.BigInteger, sa.ForeignKey('ecoms.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
    )
    op.create_table(
        'item_categories',
        sa.Column('item_id', sa.BigInteger, sa.ForeignKey('items.id'), nullable=False),
        sa.Column('category_id', sa.BigInteger, sa.ForeignKey('categories.id'), nullable=False),
    )
    op.create_table(
        'execution_item_stocks',
        sa.Column('execution_id', sa.BigInteger, sa.ForeignKey('executions.id'), nullable=False),
        sa.Column('item_id', sa.BigInteger, sa.ForeignKey('items.id'), nullable=False),
        sa.Column('stock', sa.Integer, nullable=False, server_default='1'),
    )
    


def downgrade():
    op.drop_table('execution_item_stocks')
    op.drop_table('item_categories')
    op.drop_table('items')
    op.drop_table('categories')
    op.drop_table('executions')
    op.drop_table('ecoms')
