from datetime import date, timedelta
import uuid
from flask import abort
from .models import Habit, HabitLog
from . import db

def create_habit(name, description=None):
    new_habit = Habit(
        id=uuid.uuid4(),
        name=name,
        description=description
    )

    db.session.add(new_habit)
    db.session.commit()

    return new_habit

def delete_habit(habit_id):
    habit = db.session.get(Habit, habit_id)

    if not habit:
        abort(404, description="Habit not found")

    db.session.delete(habit)
    db.session.commit()


def log_habit(habit_id, completed_date):
    habit = db.session.get(Habit, habit_id)

    if not habit:
        abort(404, description="Habit not found")

    # Prevent future date
    if completed_date > date.today():
        raise ValueError("Cannot log future date")

    # Prevent duplicate
    existing_log = HabitLog.query.filter_by(
        habit_id=habit_id,
        completed_date=completed_date
    ).first()

    if existing_log:
        raise ValueError("Already logged for this date")

    new_log = HabitLog(
        habit_id=habit_id,
        completed_date=completed_date
    )

    db.session.add(new_log)
    db.session.commit()

    return calculate_streak(habit_id)

def calculate_streak(habit_id):
    logs = HabitLog.query.filter_by(
        habit_id=habit_id
    ).order_by(HabitLog.completed_date.desc()).all()

    streak = 0
    expected_date = date.today()

    for log in logs:
        if log.completed_date == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        else:
            break

    return streak

def get_all_habits():
    habits = Habit.query.all()

    return [
        {
            "id": str(habit.id),
            "name": habit.name,
            "description": habit.description,
            "current_streak": calculate_streak(habit.id)
        }
        for habit in habits
    ]

def get_habit_with_streak(habit):
    return {
        "id": str(habit.id),
        "name": habit.name,
        "description": habit.description,
        "current_streak": calculate_streak(habit.id)
    }