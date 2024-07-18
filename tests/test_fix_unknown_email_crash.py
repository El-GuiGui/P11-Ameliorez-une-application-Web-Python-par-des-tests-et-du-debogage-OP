import pytest
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_unknown_email(client):
    response = client.post("/showSummary", data={"email": "unknown@example.com"}, follow_redirects=True)
    decoded_response = response.data.decode("utf-8")
    assert "Sorry, that email wasn&#39;t found." in decoded_response
