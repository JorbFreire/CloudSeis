from marshmallow import Schema, fields, validate


class WorkflowCreateSchema(Schema):
    name = fields.String(required=True)
    parentType = fields.String(
        required=True,
        # *** No "datasetId" becouse datasets should not be
        # *** created or modified in the route layer
        validate=validate.OneOf(["projectId", "lineId"])
    )


class WorkflowFileLinkUpdateSchema(Schema):
    fileLinkId = fields.Integer(required=True)


class WorkflowOutputNameUpdateSchema(Schema):
    outputName = fields.String(required=True)
