import pytest
from server import app, clubs, competitions


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_purchase_places(client):
    initial_club_points = int(clubs[0]["points"])
    initial_competition_places = int(competitions[0]["numberOfPlaces"])

    response = client.post(
        "/purchasePlaces",
        data={"club": clubs[0]["name"], "competition": competitions[0]["name"], "places": "1"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(clubs[0]["points"]) == initial_club_points - 1
    assert int(competitions[0]["numberOfPlaces"]) == initial_competition_places - 1


def test_purchase_places_not_enough_points(client):
    club = clubs[0]
    club["points"] = "0"
    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competitions[0]["name"], "places": "1"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Not enough points to complete the booking." in response.data
    assert int(club["points"]) == 0
