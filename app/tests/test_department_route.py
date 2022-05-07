import json
import pytest
from app.main import create_app

department = {
    "university_id": 2,
    "name": "Estudios Hispanicos",
    "classification": "ESPA",
}

# Admin account credentials
admin_account = {
    "email": "admin@account.com",
    "password": "admin"
}

user_account = {
    "email": "testjulian2@test.com",
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
def userSessionID(client):
    admin = client.post('classTrack/login', json=admin_account)
    assert type(admin.get_data()) == bytes

    return admin.get_data().strip().decode("utf-8").replace('"', "")

@pytest.fixture
def adminSessionID(client):
    admin = client.post('classTrack/login', json=user_account)
    assert type(admin.get_data()) == bytes

    return admin.get_data().strip().decode("utf-8").replace('"', "")


def test_department_routes(client, adminSessionID):
    sessionID = adminSessionID
    # Create Deparment
    department["session_id"] = sessionID
    response = client.post('classTrack/department', json=department)

    department_id = json.loads(response.get_data().strip().decode('utf-8'))['department_id']
    assert response.status_code == 200 and type(department_id) == int

    # Get department by id
    del department["session_id"]
    response = client.get('classTrack/department/' + str(department_id))
    assert response.status_code == 200 and json.loads(response.get_data().strip().decode('utf-8')) == department

    # Update department
    department["session_id"] = sessionID
    department["classification"] = "ESPA1"
    response = client.put('classTrack/department/update/' + str(department_id), json=department)
    assert response.status_code == 200 and json.loads(response.get_data().strip().decode('utf-8'))['department_id'] == department_id

    #Delete department
    response = client.post('classTrack/department/delete/' + str(department_id), json={'session_id': sessionID})
    assert response.status_code == 200 and json.loads(response.get_data().strip().decode('utf-8'))['department_id'] == department_id

def test_get_all_departments(client):
    response = client.get('classTrack/departments')
    assert response.status_code == 200

