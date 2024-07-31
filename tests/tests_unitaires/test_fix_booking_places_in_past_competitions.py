import pytest
from server import app, clubs, competitions
from datetime import datetime, timedelta


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_booking_past_competition(client):
    past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    competitions[0]["date"] = past_date
    response = client.get(f"/book/{competitions[0]['name']}/{clubs[0]['name']}", follow_redirects=True)
    assert response.status_code == 200
    assert b"This competition is in the past and cannot be booked." in response.data

    competitions[0]["date"] = future_date


def test_booking_future_competition(client):
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    competitions[0]["date"] = future_date
    response = client.get(f"/book/{competitions[0]['name']}/{clubs[0]['name']}", follow_redirects=True)
    assert response.status_code == 200
    assert b'<button type="submit">Book</button>' in response.data
