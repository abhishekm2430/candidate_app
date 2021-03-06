"""empty message

Revision ID: 4d23ec638040
Revises: 7552f3a026fe
Create Date: 2018-10-11 22:18:58.088510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d23ec638040'
down_revision = '7552f3a026fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('candidates', 'foo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidates', sa.Column('foo', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
