"""re-add-password-column-at-users_table-as-large-binary

Revision ID: d4e8ab820aff
Revises: f3191b8ca4d3
Create Date: 2024-05-28 17:02:29.649878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4e8ab820aff'
down_revision = 'f3191b8ca4d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.LargeBinary(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_table', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
