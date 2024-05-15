from marshmallow import Schema, fields, validate


class WorkflowShowSchema(Schema):
    # *** route params
    id = fields.Number(required=True)


class WorkflowCreateSchema(Schema):
    name = fields.String(required=True)
    parentType = fields.String(
        required=True,
        # *** No "datasetId" becouse datasets should not be
        # *** created or modified in the route layer
        validate=validate.OneOf(["projectId", "lineId"])
    )


class WorkflowUpdateSchema(WorkflowShowSchema):
    name = fields.String(required=True)


class WorkflowDeleteSchema(WorkflowShowSchema):
    pass
