from marshmallow import Schema, fields


class ProgramGroupCreateSchema(Schema):
    name = fields.String(required=False)
    description = fields.String(required=True)
