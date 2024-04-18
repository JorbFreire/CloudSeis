from marshmallow import Schema, fields


class CommandShowtSchema(Schema):
    # *** route params
    id = fields.Number(required=True)


class CommandCreateSchema(Schema):
    name = fields.String(required=True)
    # ! maybe should validate if it is a stringfied json
    parameters = fields.String(required=True)
    # *** route params
    workflowId = fields.Number(required=True)


class CommandUpdateParametersSchema(CommandShowtSchema):
    # ! maybe should validate if it is a stringfied json
    parameters = fields.String(required=True)


class CommandsUpdateOrderSchema(Schema):
    newOrder = fields.List(cls_or_instance=fields.Integer, required=True)
    # *** route params
    workflowId = fields.Number(required=True)


class CommandDeleteSchema(CommandShowtSchema):
    pass
