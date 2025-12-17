from marshmallow import fields, Schema

class NotesSchema(Schema):
    id=fields.Int(dump_only=True)
    data=fields.Str()
    date= fields.DateTime(dump_only=True)
    user_id= fields.Int()