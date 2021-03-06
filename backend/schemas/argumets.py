from typing import Any, Dict, Optional, Tuple

from marshmallow import EXCLUDE, Schema, ValidationError, fields, pre_load
from marshmallow.validate import Length

from backend.schemas.models import MessageSchema, UserSchema


def validate_by_defined_schema(
    schema: Schema, data: Dict[str, Any], only_fields: Tuple[fields.Field], partial=False
) -> Optional[Dict[str, Any]]:
    _schema = schema(unknown=EXCLUDE, only=only_fields, partial=partial)
    if errors := _schema.validate(data):
        raise ValidationError(errors)

    return data


class PostMessageSchema(Schema):
    recipient = fields.Integer(required=True)

    @pre_load
    def _pre_load(self, data, *_args, **_kwargs):
        return validate_by_defined_schema(MessageSchema, data, self.opts.additional)

    class Meta:
        unknown = EXCLUDE
        additional = ("subject", "body")


class SearchMessagesSchema(Schema):
    recipient = fields.Integer()

    @pre_load
    def _pre_load(self, data, *_args, **_kwargs):
        return validate_by_defined_schema(MessageSchema, data, self.opts.additional, partial=True)

    class Meta:
        unknown = EXCLUDE
        additional = ("created_at", "is_read", "owner", "subject")


class SearchUsersSchema(Schema):
    @pre_load
    def _pre_load(self, data, *_args, **_kwargs):
        return validate_by_defined_schema(UserSchema, data, self.opts.additional, partial=True)

    class Meta:
        unknown = EXCLUDE
        additonal = ("name", "email")


# Schemas to auto generate docs
class CreateUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(
        validate=Length(min=8, error="Short password. Minimum {min} characters."), required=True,
    )


class LoginSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    email = fields.Email(required=True)
    password = fields.String(
        validate=Length(min=8, error="Short password. Minimum {min} characters."), required=True,
    )
