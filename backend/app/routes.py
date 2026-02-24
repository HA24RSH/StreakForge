from flask import Blueprint, request, jsonify
from .schemas import HabitSchema, HabitLogSchema
from .services import create_habit, delete_habit, get_all_habits, get_habit_with_streak, log_habit
from .models import Habit
from marshmallow import ValidationError

habit_bp = Blueprint("habits", __name__)

habit_schema = HabitSchema()
log_schema = HabitLogSchema()


@habit_bp.route("/habits", methods=["POST"])
def create_habit_route():
    try:
        data = habit_schema.load(request.json)
        habit = create_habit(**data)
        return habit_schema.dump(habit), 201
    except ValidationError as err:
        return {"error": err.messages}, 400


@habit_bp.route("/habits/<uuid:habit_id>/log", methods=["POST"])
def log_habit_route(habit_id):
    try:
        data = log_schema.load(request.json)
        streak = log_habit(habit_id, data["completed_date"])
        return {"streak": streak}, 200
    except Exception as e:
        return {"error": str(e)}, 400
    
@habit_bp.route("/habits", methods=["GET"])
def get_habits_route():
    habits = get_all_habits()
    return habits, 200

@habit_bp.route("/habits/<uuid:habit_id>", methods=["GET"])
def get_single_habit_route(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    return get_habit_with_streak(habit), 200

@habit_bp.route("/habits/<uuid:habit_id>", methods=["DELETE"])
def delete_habit_route(habit_id):
    delete_habit(habit_id)
    return {"message": "Habit deleted"}, 200