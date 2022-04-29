import json
import pytest
from app.main import create_app

# Global Variables
test_user = {
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
def login(client):
    # Login user to get SessionID
    user = client.post('classTrack/login', json=test_user)
    assert type(user.get_data()) == bytes

    sessionID = user.get_data().strip().decode('utf-8').replace('"', "")

    return sessionID

@pytest.fixture
def user_id(client, login):
    # Get user id dynamically
    response = client.post('classTrack/me', json={'session_id': login})
    user_id = json.loads(
        response.get_data().strip().decode("utf-8"))['user_id']
    return user_id


def test_create_curriculum_rating(client, login, user_id):
    rating = {
        'user_id': user_id,
        'curriculum_id': 'CIIC_123_V1',
        'rating': 4,
        'session_id': login
    }

    # Create rating
    response = client.post('classTrack/curriculum_rating',
                           json=rating)
    
    rating_id = json.loads(
        response.get_data().strip().decode("utf-8"))['rating_id']
    assert response.status_code == 200 and type(rating_id) == int

    # Read rating by id
    response = client.get('classTrack/curriculum_rating/' + str(rating_id))

    # Removing rating['session_id'] to prevent making a copy of the whole rating object
    del rating['session_id']
    assert response.status_code == 200 and json.loads(response.get_data().strip().decode("utf-8")) == rating

    # Putting session_id inside of rating again since we will need it for later json inputs
    rating['session_id'] = login

    # Update curriculum rating
    rating['rating'] = 3
    response = client.put('classTrack/curriculum_rating/update/' + str(rating_id), json=rating)
    assert response.status_code == 200 and json.loads(response.get_data().strip().decode("utf-8"))['rating_id'] == rating_id

    # Delete curriculum rating
    response = client.post('classTrack/curriculum_rating/delete/' + str(rating_id), json=rating)
    assert response.status_code == 200 and json.loads(response.get_data().strip().decode("utf-8"))['rating_id'] == rating_id


