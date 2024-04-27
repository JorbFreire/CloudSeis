"""empty message

Revision ID: 4dab71e7f3ef
Revises: 176c12daa1b7
Create Date: 2023-09-20 17:29:31.095422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dab71e7f3ef'
down_revision = '176c12daa1b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workflow_parents_association_table',
    sa.Column('workflowId', sa.Integer(), nullable=False),
    sa.Column('lineId', sa.Integer(), nullable=True),
    sa.Column('projectId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lineId'], ['projects_table.id'], name='FK_workflow_parents_association_table_lines_table'),
    sa.ForeignKeyConstraint(['projectId'], ['lines_table.id'], name='FK_workflow_parents_association_table_projects_table'),
    sa.ForeignKeyConstraint(['workflowId'], ['workflows_table.id'], name='FK_workflow_parents_association_table_workflows_table'),
    sa.PrimaryKeyConstraint('workflowId')
    )
    with op.batch_alter_table('workflows_table', schema=None) as batch_op:
        batch_op.drop_constraint('FK_lines_table_workflows_table', type_='foreignkey')
        batch_op.drop_column('lineId')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workflows_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lineId', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('FK_lines_table_workflows_table', 'lines_table', ['lineId'], ['id'])

    op.drop_table('workflow_parents_association_table')
    # ### end Alembic commands ###