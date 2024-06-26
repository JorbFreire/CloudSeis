"""remove-password-column-at-users_table

Revision ID: f3191b8ca4d3
Revises: eee014136bfe
Create Date: 2024-05-28 17:01:44.522573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f3191b8ca4d3'
down_revision = 'eee014136bfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_table', schema=None) as batch_op:
        batch_op.drop_column('hashPassword')
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('hashPassword', postgresql.BYTEA(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
