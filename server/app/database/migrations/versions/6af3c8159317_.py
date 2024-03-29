"""empty message

Revision ID: 6af3c8159317
Revises: 416dfc18b3d9
Create Date: 2024-01-05 22:33:25.281005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6af3c8159317'
down_revision = '416dfc18b3d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('datasets_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('currentSate', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('datasets_table', schema=None) as batch_op:
        batch_op.drop_column('currentSate')

    # ### end Alembic commands ###
