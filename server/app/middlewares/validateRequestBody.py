from flask import request
from marshmallow import EXCLUDE


def validateRequestBody(routeFunction, SerializerSchema):
    def wrapper(*args, **kwargs):
        data = request.get_json()
        view_args = request.view_args

        for key, value in view_args.items():
            data.update({key: value})

        # *** unexpected fields on request body will be
        # *** excluded and ignored, not raising any error.
        SerializerSchema(unknown=EXCLUDE).load(data)

        routeFunction(*args, **kwargs)
    return wrapper
