"""commands dataset

Revision ID: 29842d62934e
Revises: 582c08edac4b
Create Date: 2024-02-21 22:06:56.912409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29842d62934e'
down_revision = '582c08edac4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('datasets_table', schema=None) as batch_op:
        batch_op.drop_constraint('FK_projects_datasets', type_='foreignkey')
        batch_op.create_foreign_key('FK_projects_datasets', 'projects_table', ['projectId'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('datasets_table', schema=None) as batch_op:
        batch_op.drop_constraint('FK_projects_datasets', type_='foreignkey')
        batch_op.create_foreign_key('FK_projects_datasets', 'datasets_table', ['projectId'], ['id'])

    # ### end Alembic commands ###
