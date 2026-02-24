from marshmallow import Schema, fields, validates, ValidationError


class HabitSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Habit name cannot be empty.")
        if len(value) > 100:
            raise ValidationError("Habit name too long.")


class HabitLogSchema(Schema):
    completed_date = fields.Date(required=True, data_key="date")