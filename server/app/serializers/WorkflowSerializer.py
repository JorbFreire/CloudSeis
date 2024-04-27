from marshmallow import Schema, fields, validate


class WorkflowShowSchema(Schema):
    # *** route params
    id = fields.Number(required=True)


class WorkflowCreateSchema(Schema):
    name = fields.String(required=True)
    parentType = fields.String(
        required=True,
        validate=validate.OneOf(["projectId", "lineId", "datasetId"])
    )


class WorkflowUpdateSchema(WorkflowShowSchema):
    name = fields.String(required=True)


class WorkflowDeleteSchema(WorkflowShowSchema):
    pass