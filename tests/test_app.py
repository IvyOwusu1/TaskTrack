import sys
import os
import pytest
import sqlite3

# allow pytest to find app.py in the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, init_db


@pytest.fixture
def client():
    app.config['TESTING'] = True

    # Recreate a fresh database for each test
    if os.path.exists("database.db"):
        os.remove("database.db")

    init_db()

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_add_and_delete_task(client):
    # Add task
    client.post("/add", data={"task": "Test Task"})

    # Get task ID from database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE title = ?", ("Test Task",))
    task = cursor.fetchone()
    conn.close()

    assert task is not None  # ensure task exists

    task_id = task[0]

    # Delete task using actual ID
    response = client.get(f"/delete/{task_id}")

    assert response.status_code == 302  # should redirect after 


def test_toggle_task(client):
    client.post("/add", data={"task": "Toggle Task"})

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE title = ?", ("Toggle Task",))
    task_id = cursor.fetchone()[0]
    conn.close()

    response = client.get(f"/toggle/{task_id}")

    assert response.status_code == 302  # should redirect after toggling