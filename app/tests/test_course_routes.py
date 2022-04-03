import json
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


def test_course_routes(client):
    # Login to admin account
    admin = client.post('classTrack/login', json=admin_account)
    assert type(admin.get_data()) == bytes

    course['session_id'] = admin.get_data().strip().decode("utf-8").replace('"', "")

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
    course['session_id'] = admin.get_data().strip().decode("utf-8").replace('"', "")
    course["name"] = "Databases2"
    course["classification"] = "CIIC-5060"

    response = client.put('classTrack/course/update/' + str(course_id),
                          json=course)
    assert response.status_code == 200 and type(course_id) == int

    # Delete course
    response = client.post('classTrack/course/delete/' + str(course_id), json=course)
    assert response.status_code == 200 and type(course_id) == int


# def test_get_all_courses(client):
#     response = client.get('classTrack/courses')
#     assert response.status_code == 200


# def test_update_course(client):
#     course = {
#         "course_id": 4,
#         "department_id": 2,
#         "name": "Databases2",
#         "classification": "CIIC-5060"
#     }

#     # Login to admin account
#     admin = client.post('classTrack/login', json=admin_account)
#     assert type(admin.get_data()) == bytes

#     headers = {
#         'SessionID': admin.get_data().strip().decode("utf-8").replace('"', "")
#     }

#     # Update course
#     response = client.put('classTrack/course/update/4',
#                           json=course, headers=headers)
#     assert response.status_code == 200

# def test_delete_course(client):
#     response = client.post('classTrack/course/delete/4')
#     assert response.status_code == 200
