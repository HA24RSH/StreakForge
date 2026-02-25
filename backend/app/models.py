import uuid
from datetime import datetime, UTC
from . import db


class Habit(db.Model):
    __tablename__ = "habits"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    logs = db.relationship(
        "HabitLog",
        backref="habit",
        cascade="all, delete",
        lazy=True,
    )


class HabitLog(db.Model):
    __tablename__ = "habit_logs"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    habit_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("habits.id"),
        nullable=False,
    )

    completed_date = db.Column(db.Date, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "habit_id",
            "completed_date",
            name="unique_habit_date",
        ),
    )