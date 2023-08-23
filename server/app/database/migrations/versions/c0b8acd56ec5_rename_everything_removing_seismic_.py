"""rename-everything-removing-seismic-overused-prefix

Revision ID: c0b8acd56ec5
Revises: d225264fcb11
Create Date: 2023-08-17 20:51:17.800847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0b8acd56ec5'
down_revision = 'd225264fcb11'
branch_labels = None
depends_on = None

# ! It's a bad pratice to create and drop all this tables again once the goal is
# ! rename the tables. However, it will take a lot of work to write it manualy
# ! once SQL alquemy does not detect this changes as table renames. This version
# ! is also not on production.
# ! For these reasons, keeping the bad practice.


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects_table',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('userId', sa.Uuid(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['userId'], ['users_table.id'], name='FK_users_table_projects_table'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('lines_table',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('projectId', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['projectId'], ['projects_table.id'], name='FK_projects_table_lines_table'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('workflows_table',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('file_name', sa.String(), nullable=True),
                    sa.Column('lineId', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['lineId'], ['lines_table.id'], name='FK_lines_table_workflows_table'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('commands_table',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('parameters', sa.Text(), nullable=True),
                    sa.Column('workflowId', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['workflowId'], [
                        'workflows_table.id'], name='FK_workflows_table_commands_table'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_table('seismic_workflows_table')
    op.drop_table('seismic_projects_table')
    op.drop_table('seismic_lines_table')
    op.drop_table('seismic_commands_table')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seismic_commands_table',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.VARCHAR(), nullable=True),
                    sa.Column('parameters', sa.TEXT(), nullable=True),
                    sa.Column('seismicCommandId', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(['seismicCommandId'], [
                        'seismic_workflows_table.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('seismic_lines_table',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.VARCHAR(), nullable=True),
                    sa.Column('seismicProjectId', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(['seismicProjectId'], [
                        'seismic_projects_table.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('seismic_projects_table',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.VARCHAR(), nullable=True),
                    sa.Column('userId', sa.CHAR(length=32), nullable=True),
                    sa.ForeignKeyConstraint(['userId'], ['users_table.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('seismic_workflows_table',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.VARCHAR(), nullable=True),
                    sa.Column('seismic_file_name',
                              sa.VARCHAR(), nullable=True),
                    sa.Column('seismicLineId', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['seismicLineId'], ['seismic_lines_table.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_table('commands_table')
    op.drop_table('workflows_table')
    op.drop_table('lines_table')
    op.drop_table('projects_table')
    # ### end Alembic commands ###