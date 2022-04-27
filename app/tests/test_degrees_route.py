import json
import pytest
from app.main import create_app

degree = {
    "department_id": 2,
    "name": "Estudios Hispanicos",
    "curriculum_sequence": "ESPA_user",
    "length": 4,
    "credits": 100
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


def test_degree_routes(client, sessionID):
    degree['session_id'] = sessionID

    # Create degree
    response = client.post('classTrack/degree', json=degree)

    degree_id = json.loads(
        response.get_data().strip().decode("utf-8"))['degree_id']

    assert response.status_code == 200 and type(degree_id) == int

    # Read degree by id

    del degree['session_id']
    response = client.get('classTrack/degree/' + str(degree_id))
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode("utf-8")) == degree

    # Update degree
    degree['session_id'] = sessionID
    degree["name"] = "Databases2"
    degree["curriculum_sequence"] = "CIIC-5060"

    response = client.put('classTrack/degree/update/' + str(degree_id),
                          json=degree)
    assert response.status_code == 200 and json.loads(response.get_data().strip().decode('utf-8'))['degree_id'] == degree_id

    # Delete degree
    response = client.post('classTrack/degree/delete/' + str(degree_id), json=degree)
    assert response.status_code == 200 and json.loads(response.get_data().strip().decode('utf-8'))['degree_id'] == degree_id

def test_get_all_degrees(client):
    response = client.get('classTrack/degrees')
    assert response.status_code == 200