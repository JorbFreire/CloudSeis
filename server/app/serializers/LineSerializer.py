from marshmallow import Schema, fields


class LineCreateSchema(Schema):
    name = fields.String(required=True)
    projectId = fields.Number(required=True)


class LineUpdateSchema(Schema):
    name = fields.String(required=True)
