from marshmallow import Schema, fields


class ProjectCreateSchema(Schema):
    name = fields.String(required=True)


class ProjectUpdateSchema():
    name = fields.String(required=True)
