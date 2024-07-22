import pytest
from server import app, clubs, competitions
from datetime import datetime, timedelta


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def setup_club_and_competition():
    club = clubs[0]
    competition = competitions[0]
    club["points"] = "20"
    competition["numberOfPlaces"] = "25"
    competition["date"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    if "bookings" in competition:
        competition["bookings"] = {}
    return club, competition


def test_purchase_places(client):
    club, competition = setup_club_and_competition()
    initial_club_points = int(club["points"])
    initial_competition_places = int(competition["numberOfPlaces"])

    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "1"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == initial_club_points - 1
    assert int(competition["numberOfPlaces"]) == initial_competition_places - 1


def test_purchase_places_not_enough_points(client):
    club, competition = setup_club_and_competition()
    club["points"] = "0"
    initial_club_points = int(club["points"])

    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "1"},
        follow_redirects=True,
    )

    print(response.data)

    assert response.status_code == 200
    assert b"Not enough points to complete the booking." in response.data
    assert int(club["points"]) == initial_club_points
