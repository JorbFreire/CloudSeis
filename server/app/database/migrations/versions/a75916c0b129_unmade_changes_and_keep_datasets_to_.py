"""unmade changes and keep datasets to worklfowmodel

Revision ID: a75916c0b129
Revises: 7c11533db05a
Create Date: 2024-07-09 18:13:41.941552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a75916c0b129'
down_revision = '7c11533db05a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workflows_table', schema=None) as batch_op:
        batch_op.drop_column('parentType')
        batch_op.drop_column('parentId')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workflows_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parentId', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('parentType', sa.VARCHAR(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###