"""add-program_id-column-to-commands_table

Revision ID: 9dba7985d438
Revises: a8fe9e953e92
Create Date: 2024-07-30 12:41:15.023851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dba7985d438'
down_revision = 'a8fe9e953e92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commands_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('program_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('FK_programs_table_commands_table', 'programs_table', ['program_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commands_table', schema=None) as batch_op:
        batch_op.drop_constraint('FK_programs_table_commands_table', type_='foreignkey')
        batch_op.drop_column('program_id')

    # ### end Alembic commands ###