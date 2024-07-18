import pytest
from server import app, clubs, competitions
from datetime import datetime, timedelta


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_booking_more_than_12_places(client):
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    competitions[0]["date"] = future_date

    response = client.post(
        "/purchasePlaces",
        data={"club": clubs[0]["name"], "competition": competitions[0]["name"], "places": "13"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You cannot book more than 12 places." in response.data


def test_booking_total_more_than_12_places(client):
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    competitions[0]["date"] = future_date

    response = client.post(
        "/purchasePlaces",
        data={"club": clubs[0]["name"], "competition": competitions[0]["name"], "places": "6"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    response = client.post(
        "/purchasePlaces",
        data={"club": clubs[0]["name"], "competition": competitions[0]["name"], "places": "7"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"You cannot book more than 12 places in total for this competition." in response.data
