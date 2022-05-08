import copy
import json
import pytest
from app.main import create_app
from app.tests.testVars import *

# Global Variables
test_user = {
    "email": "juliantest2@test.com",
    "password": "test"
}

curriculum = testCurriculum

test_output = copy.deepcopy(curriculum)


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
    # Login user to get SessionID
    user = client.post('classTrack/login', json=test_user)
    assert type(user.get_data()) == bytes

    return user.get_data().strip().decode('utf-8').replace('"', "")

@pytest.fixture
def user_id(client, sessionID):
    # Get user id dynamically
    response = client.post('classTrack/me', json={'session_id': sessionID})
    user_id = json.loads(
        response.get_data().strip().decode("utf-8"))['user_id']
    return user_id


def test_curriculum_routes(client, sessionID):
    response = client.post('classTrack/me', json={'session_id': sessionID})
    user_id = json.loads(
        response.get_data().strip().decode("utf-8"))["user_id"]

    curriculum['user_id'] = user_id
    curriculum['session_id'] = sessionID

    # Create curriculum
    response = client.post('classTrack/curriculum',
                           json=curriculum)

    # response.get_data().strip().decode("utf-8"))['curriculum_id']
    curriculum_id = json.loads(response.get_data().strip().decode("utf-8"))
    
    assert response.status_code == 200 and type(curriculum_id) == str

    # Adding curriculum_id to the base curriculum json so that we can check later on if its the same as the one found in the DB
    curriculum["curriculum_id"] = curriculum_id

    # Read rating by id
    response = client.get('classTrack/curriculum/' + curriculum_id)
    curriculum_output = json.loads(response.get_data().strip().decode("utf-8"))

    # Removing curriculum['session_id'] to prevent making a copy of the whole curriculum object
    # Removing deptCode because still don't know what is the purpose for it
    del curriculum['session_id'], curriculum['deptCode']
    # Checking if curriculum output is correct
    course_count = 0
    for semester in curriculum['graph'][0]['semesters']:
        if len(semester) == 4:
            course_count += len(semester["courses"])

    test_output['user_id'] = user_id
    test_output['curriculum_id'] = curriculum_id
    test_output['course_count'] = course_count
    test_output['rating'] = 0
    test_output['semesters'] = len(curriculum['graph'][0]['semesters'])
    assert response.status_code == 200 and test_output == curriculum_output

    # Putting session_id inside of curriculum again since we will need it for later json inputs
    curriculum['session_id'] = sessionID

    # Update curriculum
    curriculum['rating'] = 3
    response = client.put('classTrack/curriculum/update/' +
                          str(curriculum_id), json=curriculum)
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode("utf-8"))['curriculum_id'] == curriculum_id

    # Delete curriculum
    response = client.post('classTrack/curriculum/delete/' +
                           str(curriculum_id), json=curriculum)
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode("utf-8"))['curriculum_id'] == curriculum_id
