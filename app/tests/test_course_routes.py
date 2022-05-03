import json
import time
import pytest
from app.main import create_app

course = {
    "department_id": 2,
    "name": "Databases",
    "classification": "CIIC-4060"
}

# Admin account credentials
admin_account = {
    "email": "admin@account.com",
    "password": "admin"
}

error_account = {
    "email": "error@account.com",
    "password": "test"
}

user_account = {
    "email": "juliantest2@test.com",
    "password": "test"
}

sessionM = {
    "err": "Invalid Session"
}

userM = {
    "err": "User is not an admin. They are a student"
}

universityM = {
    "err": "University is not administered by this user"
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
    user = client.post('classTrack/login', json=user_account)
    assert type(user.get_data()) == bytes

    return user.get_data().strip().decode("utf-8").replace('"', "")

def create_course(cli, session):
    cse = {
        "department_id": 2,
        "name": "Databases",
        "classification": "CIIC-4060"
    }

    sessionID = session
    cse["session_id"] = sessionID
    # Create course
    response = cli.post('classTrack/course', json=cse)

    course_id = json.loads(
        response.get_data().strip().decode("utf-8"))['course_id']

    return course_id


def delete_course(client, adminSessionID, course_id):
    course["session_id"] = adminSessionID
    # Delete course
    response = client.post('classTrack/course/delete/' +
                           str(course_id), json=course)
    assert response.status_code == 200 and type(course_id) == int


def test_course_routes(client, adminSessionID):
    sessionID = adminSessionID
    course['session_id'] = sessionID

    # Create course
    response = client.post('classTrack/course', json=course)

    course_id = json.loads(
        response.get_data().strip().decode("utf-8"))['course_id']

    assert response.status_code == 200 and type(course_id) == int

    # Read course by id

    del course['session_id']
    course["course_id"] = course_id
    response = client.get('classTrack/course/' + str(course_id))
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode("utf-8")) == course

    # Update course
    course['session_id'] = sessionID
    course["name"] = "Databases2"
    course["classification"] = "CIIC-5060"

    response = client.put('classTrack/course/update/' + str(course_id),
                          json=course)
    assert response.status_code == 200 and type(course_id) == int

    # Delete course
    response = client.post('classTrack/course/delete/' +
                           str(course_id), json=course)
    assert response.status_code == 200 and type(course_id) == int


def test_create_course_user_error(client, userSessionID):
    sessionID = userSessionID
    course['session_id'] = sessionID

    # Create course
    response = client.post('classTrack/course', json=course)

    error = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 403 and error == userM


def test_create_course_invalid_session(client):
    course['session_id'] = "Error session"

    # Create course
    response = client.post('classTrack/course', json=course)

    error = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 401 and error == sessionM


def test_create_course_department_notfound(client, adminSessionID):
    sessionID = adminSessionID
    course['session_id'] = sessionID
    course['department_id'] = 3

    # Create course
    response = client.post('classTrack/course', json=course)

    error = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 404 and error == {
        "err": "Department not found"}


def test_create_course_university_error(client):
    # Log in
    account = client.post('classTrack/login', json=error_account)
    sessionID = account.get_data().strip().decode("utf-8").replace('"', "")
    course['session_id'] = sessionID
    course["department_id"] = 2

    # Create course
    response = client.post('classTrack/course', json=course)

    error = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 404 and error == universityM


def test_get_course_error(client):
    # Read course by id
    response = client.get('classTrack/course/' + "0")
    assert response.status_code == 404 and json.loads(
        response.get_data().strip().decode("utf-8")) == {"err": "Course not found"}


def test_update_course_user_error(client, userSessionID, adminSessionID):
    course_id = create_course(client, adminSessionID)

    sessionID = userSessionID
    course['session_id'] = sessionID
    course["name"] = "Databases2"
    course["classification"] = "CIIC-5060"

    response = client.put('classTrack/course/update/' + str(course_id),
                          json=course)
    error = response.get_data().strip().decode("utf-8")

    assert response.status_code == 403 and error == userM

    delete_course(client, adminSessionID, course_id)


def test_update_course_invalid_session(client, adminSessionID):
    course_id = create_course(client, adminSessionID)

    course['session_id'] = "Error session"
    course["name"] = "Databases2"
    course["classification"] = "CIIC-5060"

    response = client.put('classTrack/course/update/' + str(course_id),
                          json=course)
    error = json.loads(response.get_data().strip().decode("utf-8"))

    assert response.status_code == 401 and error == sessionM

    delete_course(client, adminSessionID, course_id)


def test_update_course_department_notfound(client, adminSessionID):
    sessionID = adminSessionID
    course['session_id'] = sessionID
    course['department_id'] = 3

    # Create course
    response = client.post('classTrack/course', json=course)

    error = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 404 and error == {
        "err": "Department not found"}


def test_update_course_university_error(client):
    # Log in
    account = client.post('classTrack/login', json=error_account)
    sessionID = account.get_data().strip().decode("utf-8").replace('"', "")
    course['session_id'] = sessionID
    course["department_id"] = 2

    # Create course
    response = client.post('classTrack/course', json=course)

    error = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 404 and error == {
        "err": "University is not administered by this user"}
