
import pytest
from app import app, members


@pytest.fixture
def client():
    app.config["TESTING"] = True
    members.clear()

    with app.test_client() as client:
        yield client

    members.clear()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["application"] == "ACEest Fitness & Gym"
    assert response.json["version"] == "1.0"


def test_register_member(client):
    response = client.post(
        "/register",
        json={"name": "Arun", "age": 25}
    )

    assert response.status_code == 201
    assert response.json["member"]["name"] == "Arun"


def test_register_member_missing_name(client):
    response = client.post(
        "/register",
        json={"age": 25}
    )

    assert response.status_code == 400


def test_register_member_invalid_age(client):
    response = client.post(
        "/register",
        json={"name": "Arun", "age": "invalid"}
    )

    assert response.status_code == 400


def test_register_member_negative_age(client):
    response = client.post(
        "/register",
        json={"name": "Arun", "age": -5}
    )

    assert response.status_code == 400


def test_get_members(client):
    client.post(
        "/register",
        json={"name": "Arun", "age": 25}
    )

    response = client.get("/members")

    assert response.status_code == 200
    assert len(response.json) == 1


def test_calculate_bmi(client):
    response = client.post(
        "/bmi",
        json={"weight": 70, "height": 1.75}
    )

    assert response.status_code == 200
    assert response.json["bmi"] == 22.86
    assert response.json["category"] == "Normal"


def test_calculate_bmi_invalid_input(client):
    response = client.post(
        "/bmi",
        json={"weight": 70, "height": 0}
    )

    assert response.status_code == 400

