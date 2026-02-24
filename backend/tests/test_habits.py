import json
from datetime import date
from logging import log


def test_create_habit(client):
    response = client.post(
        "/habits",
        json={"name": "Read", "description": "Read daily"},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Read"


def test_empty_name_validation(client):
    response = client.post(
        "/habits",
        json={"name": "", "description": "Invalid"},
    )

    assert response.status_code == 400


def test_log_habit_and_streak(client):
    create = client.post("/habits", json={"name": "Workout"})
    habit_id = create.get_json()["id"]

    today = date.today().isoformat()

    log = client.post(
        f"/habits/{habit_id}/log",
        json={"date": today},
    )

    print(log.get_json())
    print(log.status_code)
    assert log.status_code == 200
    
    assert log.get_json()["streak"] == 1


def test_duplicate_log_prevented(client):
    create = client.post("/habits", json={"name": "Meditate"})
    habit_id = create.get_json()["id"]

    today = date.today().isoformat()

    client.post(f"/habits/{habit_id}/log", json={"date": today})
    duplicate = client.post(f"/habits/{habit_id}/log", json={"date": today})

    assert duplicate.status_code == 400


def test_future_date_rejected(client):
    from datetime import timedelta

    create = client.post("/habits", json={"name": "Stretch"})
    habit_id = create.get_json()["id"]

    future = (date.today() + timedelta(days=1)).isoformat()

    response = client.post(
        f"/habits/{habit_id}/log",
        json={"date": future},
    )

    assert response.status_code == 400