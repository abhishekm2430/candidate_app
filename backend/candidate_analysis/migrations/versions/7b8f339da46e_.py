"""empty message

Revision ID: 7b8f339da46e
Revises: 88d69b547cd7
Create Date: 2018-10-11 20:35:29.993479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b8f339da46e'
down_revision = '88d69b547cd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate_document_keywords',
    sa.Column('candidate_document_id', sa.Integer(), nullable=False),
    sa.Column('keyword_id', sa.Integer(), nullable=False),
    sa.Column('density', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['candidate_document_id'], ['candidate_documents.candidate_document_id'], ),
    sa.ForeignKeyConstraint(['keyword_id'], ['keywords.keyword_id'], ),
    sa.PrimaryKeyConstraint('candidate_document_id', 'keyword_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('candidate_document_keywords')
    # ### end Alembic commands ###
