"""add-unique-constraint-to-email-column-on-users-table

Revision ID: c63dc0503ed6
Revises: f30c326b68b2
Create Date: 2024-03-19 03:17:09.679768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c63dc0503ed6'
down_revision = 'f30c326b68b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_table', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_table', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###