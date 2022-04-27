import json
import pytest
from app.main import create_app

history = {
    "curriculum_id": "CIIC_57_V1",
}

# Admin account credentials
user_account = {
    "email": "test@testjulian.com",
    "password": "test"
}


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def sessionID(client):
    user = client.post('classTrack/login', json=user_account)
    assert type(user.get_data()) == bytes

    return user.get_data().strip().decode("utf-8").replace('"', "")


def test_history_routes(client, sessionID):
    history['session_id'] = sessionID

    response = client.post('classTrack/me', json={'session_id': sessionID})
    user_id = json.loads(response.get_data().strip().decode("utf-8"))['user_id']
    history['user_id'] = user_id

    # Create history
    response = client.post('classTrack/history', json=history)

    history_id = json.loads(
        response.get_data().strip().decode("utf-8"))['history_id']

    assert response.status_code == 200 and type(history_id) == int

    # Add history_id to the json object so that we can check if everything is in order
    history['history_id'] = history_id

    # Read history by id

    del history['session_id']
    response = client.get('classTrack/history/' + str(history_id))
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode("utf-8")) == history

    # Delete history and adding session id to the json object, so that we have permission to delete it from the DB
    history['session_id'] = sessionID
    response = client.post('classTrack/history/delete/' + str(history_id), json=history)
    assert response.status_code == 200 and json.loads(response.get_data().strip().decode('utf-8'))['history_id'] == history_id

def test_get_all_histories(client):
    response = client.get('classTrack/history')
    assert response.status_code == 200