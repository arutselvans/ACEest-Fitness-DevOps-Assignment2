
import pytest
from app import app, members


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = True
    members.clear()

    with app.test_client() as client:
        yield client

    members.clear()


def get_csrf_headers(client):
    response = client.get("/csrf-token")
    token = response.json["csrf_token"]

    return {
        "X-CSRFToken": token
    }


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["application"] == "ACEest Fitness & Gym"
    assert response.json["version"] == "1.0"


def test_register_member(client):
    response = client.post(
        "/register",
        json={"name": "Arun", "age": 25},
        headers=get_csrf_headers(client)
    )

    assert response.status_code == 201
    assert response.json["member"]["name"] == "Arun"


def test_register_member_missing_name(client):
    response = client.post(
        "/register",
        json={"age": 25},
        headers=get_csrf_headers(client)
    )

    assert response.status_code == 400


def test_register_member_invalid_age(client):
    response = client.post(
        "/register",
        json={"name": "Arun", "age": "invalid"},
        headers=get_csrf_headers(client)
    )

    assert response.status_code == 400


def test_register_member_negative_age(client):
    response = client.post(
        "/register",
        json={"name": "Arun", "age": -5},
        headers=get_csrf_headers(client)
    )

    assert response.status_code == 400


def test_get_members(client):
    client.post(
        "/register",
        json={"name": "Arun", "age": 25},
        headers=get_csrf_headers(client)
    )

    response = client.get("/members")

    assert response.status_code == 200
    assert len(response.json) == 1


def test_calculate_bmi(client):
    response = client.post(
        "/bmi",
        json={"weight": 70, "height": 1.75},
        headers=get_csrf_headers(client)
    )

    assert response.status_code == 200
    assert response.json["bmi"] == 22.86
    assert response.json["category"] == "Normal"


def test_calculate_bmi_invalid_input(client):
    response = client.post(
        "/bmi",
        json={"weight": 70, "height": 0},
        headers=get_csrf_headers(client)
    )

    assert response.status_code == 400


def test_register_member_without_csrf_token(client):
    response = client.post(
        "/register",
        json={"name": "Arun", "age": 25}
    )

    assert response.status_code == 400
    assert len(members) == 0


def test_calculate_bmi_invalid_numeric_input(client):
    response = client.post(
        "/bmi",
        json={"weight": "invalid", "height": 1.75},
        headers=get_csrf_headers(client)
    )

    assert response.status_code == 400
    assert response.json["error"] == "Weight and height must be numbers"


def test_calculate_bmi_underweight(client):
    response = client.post(
        "/bmi",
        json={"weight": 45, "height": 1.75},
        headers=get_csrf_headers(client)
    )

    assert response.status_code == 200
    assert response.json["category"] == "Underweight"


def test_calculate_bmi_overweight(client):
    response = client.post(
        "/bmi",
        json={"weight": 80, "height": 1.75},
        headers=get_csrf_headers(client)
    )

    assert response.status_code == 200
    assert response.json["category"] == "Overweight"


def test_calculate_bmi_obese(client):
    response = client.post(
        "/bmi",
        json={"weight": 100, "height": 1.75},
        headers=get_csrf_headers(client)
    )

    assert response.status_code == 200
    assert response.json["category"] == "Obese"

