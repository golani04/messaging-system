from marshmallow import Schema, fields


class DefaultErrorSchema(Schema):
    success = fields.Boolean()
    errors = fields.String()


class ValidationErrorSchema(Schema):
    success = fields.Boolean()
    errors = fields.Dict(
        fields.String(), fields.Dict(fields.String(), fields.List(fields.String()))
    )
