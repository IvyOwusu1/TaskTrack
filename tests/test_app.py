import sys
import os
import pytest

# allow pytest to find app.py in the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, init_db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    init_db()


    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200 