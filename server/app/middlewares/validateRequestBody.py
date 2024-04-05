from flask import request
from marshmallow import EXCLUDE


def validateRequestBody(routeFunction, SerializerSchema):
    def wrapper(*args, **kwargs):
        data = request.get_json()
        route_args = request.view_args

        for key, value in route_args.items():
            data.update({key: value})

        # *** unexpected fields on request body will be
        # *** excluded and ignored, not raising any error.
        SerializerSchema(unknown=EXCLUDE).load(data)

        response = routeFunction(*args, **kwargs)
        return response
    return wrapper
