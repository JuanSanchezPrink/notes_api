from marshmallow import Schema, fields, validates, ValidationError, validates_schema

class NoteCreateSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)

    @validates('title')
    def validate_title(self, value):
        if not value.strip():
            raise ValidationError("Title cannot be empty.")

    @validates('content')
    def validate_content(self, value):
        if not value.strip():
            raise ValidationError("Content cannot be empty.")

class NoteUpdateSchema(Schema):
    title = fields.String(required=False)
    content = fields.String(required=False)

    @validates('title')
    def validate_title(self, value):
        if value is not None and not value.strip():
            raise ValidationError("Title cannot be empty.")

    @validates('content')
    def validate_content(self, value):
        if value is not None and not value.strip():
            raise ValidationError("Content cannot be empty.")

    @validates_schema
    def validate_at_least_one_field(self, data, **kwargs):
        if not data.get('title') and not data.get('content'):
            raise ValidationError('At least one of title or content is required.')
