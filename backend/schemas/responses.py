from marshmallow import Schema, fields


TokensSchema = Schema.from_dict(
    {"access_csrf": fields.UUID(), "refresh_csrf": fields.UUID()}, name="TokensSchema"
)

AccessTokenSchema = Schema.from_dict({"access_csrf": fields.UUID()}, name="AccessTokenSchema")
