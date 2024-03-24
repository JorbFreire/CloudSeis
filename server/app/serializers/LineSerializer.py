from marshmallow import Schema, fields


class LineListSchema(Schema):
    # *** route params
    lineId = fields.Number(required=True)


class LineCreateSchema(Schema):
    name = fields.String(required=True)
    projectId = fields.Number(required=True)


class LineUpdateSchema(LineListSchema):
    name = fields.String(required=True)


class LineDeleteSchema(LineListSchema):
    pass
