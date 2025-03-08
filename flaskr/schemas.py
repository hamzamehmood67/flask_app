from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
