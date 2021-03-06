"""empty message

Revision ID: 8ff298e88039
Revises: bda58b894e66
Create Date: 2018-10-11 18:48:32.933115

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8ff298e88039'
down_revision = 'bda58b894e66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate_documents',
    sa.Column('candidate_document_id', sa.Integer(), nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.Column('document_path', sa.Text(), nullable=True),
    sa.Column('document_metadata_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('grammar_score', sa.Float(), nullable=True),
    sa.Column('document_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('technology_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('technology_category_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.candidate_id'], ),
    sa.PrimaryKeyConstraint('candidate_document_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('candidate_documents')
    # ### end Alembic commands ###
