from flask import request
from marshmallow import EXCLUDE


def validateRequestBody(routeFunction, SerializerSchema):
    def wrapper(*args, **kwargs):
        data = request.get_json()

        # *** unexpected fields on request body will be
        # *** excluded and ignored, not raising any error.
        SerializerSchema(unknown=EXCLUDE).load(data)

        response = routeFunction(*args, **kwargs)
        return response
    return wrapper
