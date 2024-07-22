import pytest
from server import app, clubs


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_points_board(client):
    response = client.get("/pointsdisplayboard")
    assert response.status_code == 200
    for club in clubs:
        assert bytes(club["name"], "utf-8") in response.data
        assert bytes(club["points"], "utf-8") in response.data
