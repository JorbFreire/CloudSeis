from marshmallow import ValidationError


class FormatError(ValidationError):
    def __init__(self, message: str):
        self.message = message
        self.statusCode = 422
