from marshmallow import Schema, fields


class ProjectListWorkflowsSchema(Schema):
    # *** route params
    id = fields.Number(required=True)


class ProjectCreateSchema(Schema):
    name = fields.String(required=True)


class ProjectUpdateSchema(ProjectListWorkflowsSchema):
    name = fields.String(required=True)


class ProjectDeleteSchema(ProjectListWorkflowsSchema):
    pass
