import json
import pytest
from app.main import create_app

university = {
    "university_id": 2,
    "name": "University of Puerto Rico - Mayaguez",
    "codification": "1234",
    "state": "Puerto Rico",
    "country": "US"
}

# Admin account credentials
admin_account = {
    "email": "admin@account.com",
    "password": "admin"
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
    admin = client.post('classTrack/login', json=admin_account)
    assert type(admin.get_data()) == bytes

    return admin.get_data().strip().decode("utf-8").replace('"', "")

def test_create_university(client, sessionID):
    response = client.post('classTrack/university', json={'session_id': sessionID})
    assert response.status_code == 403

def test_get_all_universities(client):
    response = client.get('classTrack/universities')
    assert response.status_code == 200


def test_get_university_by_id(client):
    response = client.get('classTrack/university/2')
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode("utf-8")) == university


def test_update_university(client, sessionID):
    university["state"] = "PR"
    university['session_id'] = sessionID
    response = client.put('classTrack/university/update/2', json=university)
    assert response.status_code == 200 and json.loads(response.get_data(
    ).strip().decode("utf-8"))['university_id'] == university["university_id"]

    university['state'] = "Puerto Rico"
    response = client.put('classTrack/university/update/2', json=university)
    assert response.status_code == 200 and json.loads(response.get_data(
    ).strip().decode("utf-8"))['university_id'] == university["university_id"]

def test_delete_university(client, sessionID):
    response = client.post('classTrack/university/delete/2', json={'session_id': sessionID})
    assert response.status_code == 403
