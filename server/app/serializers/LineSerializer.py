from marshmallow import Schema, fields


class LineListSchema(Schema):
    # *** route params
    projectId = fields.Number(required=True)


class LineCreateSchema(Schema):
    name = fields.String(required=True)
    projectId = fields.Number(required=True)


class LineDeleteSchema(Schema):
    # *** route params
    projectId = fields.Number(required=True)


class LineUpdateSchema(LineDeleteSchema):
    name = fields.String(required=True)
