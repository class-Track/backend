import json
import pytest
from requests import session
from app.main import create_app

# This import is for variables that would be used in almost every test
# If you see a variable that is not declared before hand, then its in this file
from app.tests.testVars import *

degree = {
    "department_id": 2,
    "name": "Estudios Hispanicos",
    "length": 4,
    "credits": 100
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
def adminSessionID(client):
    admin = client.post('classTrack/login', json=admin_account)
    assert type(admin.get_data()) == bytes

    return admin.get_data().strip().decode("utf-8").replace('"', "")


@pytest.fixture
def userSessionID(client):
    admin = client.post('classTrack/login', json=user_account)
    assert type(admin.get_data()) == bytes

    return admin.get_data().strip().decode("utf-8").replace('"', "")

# Helper functions to create and delete degrees
def create_degree(cli, session):
    dge = {
    "department_id": 2,
    "name": "Estudios Hispanicos",
    "length": 4,
    "credits": 100
}

    sessionID = session
    dge["session_id"] = sessionID
    # Create degree
    response = cli.post('classTrack/degree', json=dge)

    degreeID = json.loads(
        response.get_data().strip().decode("utf-8"))

    return degreeID


def delete_degree(client, adminSessionID, degree_id):
    degree["session_id"] = adminSessionID
    # Delete degree
    client.post('classTrack/degree/delete/' + str(degree_id), json=degree)

# Create errors
def test_create_degree_user_error(client, userSessionID):
    sessionID = userSessionID
    degree['session_id'] = sessionID

    # Create degree
    response = client.post('classTrack/degree', json=degree)

    error = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 403 and error == userM


def test_create_degree_invalid_session(client):
    degree['session_id'] = "not a session"

    # Create degree
    response = client.post('classTrack/degree', json=degree)

    error = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 401 and error == invalidSession


def test_create_degree_department_not_found(client, adminSessionID):
    sessionID = adminSessionID
    degree['session_id'] = sessionID
    degree['department_id'] = 0

    # Create degree
    response = client.post('classTrack/degree', json=degree)

    error = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 404 and error == depNotFound


def test_create_degree_university_error(client):
    # Log in
    account = client.post('classTrack/login', json=error_account)
    sessionID = account.get_data().strip().decode("utf-8").replace('"', "")
    degree['session_id'] = sessionID

    # Create degree
    response = client.post('classTrack/degree', json=degree)

    error = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 404 and error == uniError

def test_get_degree_error(client):
    response = client.get('classTrack/degree/0' )
    assert response.status_code == 404 and json.loads(
        response.get_data().strip().decode("utf-8")) == degNotFound

# Update errors
def test_update_degree_user_error(client, userSessionID, adminSessionID):
    degree_id = create_degree(client, adminSessionID)

    sessionID = userSessionID
    degree['session_id'] = sessionID
    degree["name"] = "Databases2"
    degree["length"] = 5
    degree["credits"] = 50

    response = client.put('classTrack/degree/update/' + str(degree_id),
                          json=degree)
    error = json.loads(response.get_data().strip().decode("utf-8"))

    assert response.status_code == 403 and error == userM

    delete_degree(client, adminSessionID, degree_id)


def test_update_degree_invalid_session(client, adminSessionID):
    degree_id = create_degree(client, adminSessionID)

    degree['session_id'] = "Error session"
    degree["name"] = "Databases2"
    degree["length"] = 5
    degree["credits"] = 50

    response = client.put('classTrack/degree/update/' + str(degree_id),
                          json=degree)
    error = json.loads(response.get_data().strip().decode("utf-8"))

    assert response.status_code == 401 and error == invalidSession

    delete_degree(client, adminSessionID, degree_id)


def test_update_degree_degree_not_found(client, adminSessionID):
    degree_id = create_degree(client, adminSessionID)

    degree['session_id'] = adminSessionID
    degree["name"] = "Databases2"
    degree["length"] = 5
    degree["credits"] = 50
    degree["department_id"] = 0

    response = client.put('classTrack/degree/update/' + str(degree_id),
                          json=degree)
    error = json.loads(response.get_data().strip().decode("utf-8"))

    assert response.status_code == 404 and error == depNotFound

    delete_degree(client, adminSessionID, degree_id)


def test_update_degree_university_error(client, adminSessionID):
    account = client.post('classTrack/login', json=error_account)
    sessionID = account.get_data().strip().decode("utf-8").replace('"', "")
    degree_id = create_degree(client, adminSessionID)

    degree['session_id'] = sessionID
    degree["name"] = "Databases2"
    degree["length"] = 5
    degree["credits"] = 50

    response = client.put('classTrack/degree/update/' + str(degree_id),
                          json=degree)
    error = json.loads(response.get_data().strip().decode("utf-8"))

    assert response.status_code == 404 and error == uniError

    delete_degree(client, adminSessionID, degree_id)

# Full process when it works
def test_degree_routes(client, adminSessionID):
    sessionID = adminSessionID
    degree['session_id'] = sessionID

    # Create degree
    response = client.post('classTrack/degree', json=degree)

    degree_id = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 200 and type(degree_id) == int

    degree["curriculum_sequence"] = "{}_{}_admin".format(
        degree['department_id'], degree_id)

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
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode('utf-8'))['degree_id'] == degree_id

    # Delete degree
    response = client.post('classTrack/degree/delete/' +
                           str(degree_id), json=degree)
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode('utf-8'))['degree_id'] == degree_id


def test_get_all_degrees(client):
    response = client.get('classTrack/degrees')
    assert response.status_code == 200
