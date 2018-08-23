"""empty message

Revision ID: 81a9699f83e3
Revises: 8104391f53f1
Create Date: 2018-08-09 10:47:19.350086

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '81a9699f83e3'
down_revision = '8104391f53f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book_update', 'before_data')
    op.drop_column('book_update', 'after_data')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book_update', sa.Column('after_data', mysql.TEXT(), nullable=True))
    op.add_column('book_update', sa.Column('before_data', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###
