import pytest
from server import app, clubs, competitions
from datetime import datetime, timedelta


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def setup_club_and_competition():
    # Reset stats
    club = clubs[0]
    competition = competitions[0]
    club["points"] = "20"
    competition["numberOfPlaces"] = "25"
    competition["date"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    if "bookings" in competition:
        competition["bookings"] = {}
    return club, competition


def test_booking_with_sufficient_points(client):
    club, competition = setup_club_and_competition()

    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "5"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == 15
    assert int(competition["numberOfPlaces"]) == 20


def test_purchase_negative_places(client):
    club, competition = setup_club_and_competition()

    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "-2"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"The number of places must be greater than 0." in response.data


def test_purchase_zero_places(client):
    club, competition = setup_club_and_competition()

    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "0"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"The number of places must be greater than 0." in response.data


def test_purchase_more_than_available_places(client):
    club, competition = setup_club_and_competition()
    competition["numberOfPlaces"] = "8"

    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "9"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Not enough places available in the competition." in response.data
