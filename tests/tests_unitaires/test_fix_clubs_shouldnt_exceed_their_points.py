import pytest
from server import app, clubs, competitions
from datetime import datetime, timedelta


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_booking_with_insufficient_points(client):
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    competitions[0]["date"] = future_date
    club = clubs[0]
    club["points"] = "0"

    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competitions[0]["name"], "places": "1"},
        follow_redirects=True,
    )

    print(response.data)
    assert response.status_code == 200
    assert b"Not enough points to complete the booking." in response.data


def test_booking_with_sufficient_points(client):
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    competitions[0]["date"] = future_date
    club = clubs[0]
    club["points"] = "20"
    initial_competition_places = int(competitions[0]["numberOfPlaces"])

    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competitions[0]["name"], "places": "5"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == 15  # 20 - 5
    assert int(competitions[0]["numberOfPlaces"]) == initial_competition_places - 5
