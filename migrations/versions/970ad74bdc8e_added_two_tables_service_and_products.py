"""Added two tables Service and Products

Revision ID: 970ad74bdc8e
Revises: 7d95eef7a4c0
Create Date: 2024-05-08 15:47:36.253392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '970ad74bdc8e'
down_revision = '7d95eef7a4c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=False),
    sa.Column('quantity_available', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('service')
    op.drop_table('product')
    # ### end Alembic commands ###
