import json
import pytest
from requests import session
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

def test_course_routes(client, sessionID):
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
    response = client.post('classTrack/course/delete/' + str(course_id), json=course)
    assert response.status_code == 200 and type(course_id) == int
