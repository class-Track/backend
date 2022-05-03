import json
import pytest
from app.main import create_app

# Global Variables
test_user = {
    "email": "test@testjulian.com",
    "password": "test"
}
test_admin = {
    "email": "admin@account.com",
    "password": "admin"
}


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.testing = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def login_user(client):
    login = client.post('classTrack/login', json=test_user)
    assert type(login.get_data()) == bytes

    # Removing new lines from Session ID and decoding so it could be json compatible
    user_sessionID = login.get_data().strip().decode("utf-8").replace('"', "")

    return user_sessionID


# @pytest.fixture
# def login_admin(client):
#     login = client.post('classTrack/login', json=test_admin)
#     assert type(login.get_data()) == bytes

#     # Removing new lines from Session ID and decoding so it could be json compatible
#     admin_sessionID = login.get_data().strip().decode("utf-8").replace('"', "")

#     yield admin_sessionID

def test_create_account(client):
     # Create admin account
    first_name = "Error"
    last_name = "Account"
    email = "error@account.com"
    university_id = 3
    password = "test"

    data = {
        "isAdmin": True,
        "variant_id": university_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }

    response = client.post('classTrack/user', json=data)
    admin_id = json.loads(
        response.get_data().strip().decode("utf-8"))

    assert response.status_code == 200 and type(admin_id) == int

def test_admin_routes(client):
    # Create admin account
    first_name = "Admin"
    last_name = "Account"
    email = "admin1@account.com"
    university_id = 2
    password = "admin"

    data = {
        "isAdmin": True,
        "variant_id": university_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }

    response = client.post('classTrack/user', json=data)
    admin_id = json.loads(
        response.get_data().strip().decode("utf-8"))['user_id']

    assert response.status_code == 200 and type(admin_id) == int

    # Login admin account
    login = client.post('classTrack/login', json={"email": email, "password": password})
    assert type(login.get_data()) == bytes

    sessionID = login.get_data().strip().decode("utf-8").replace('"', "")

    # Get admin by id
    admin_account = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "university_id": university_id,
        "user_id": admin_id
    }

    response = client.get('classTrack/admin/' + str(admin_id))
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode("utf-8")) == admin_account

    # Get admin by session id
    me_data = {
        "isAdmin": True,
        "university_id": university_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "user_id": admin_id
    }
    response = client.post('classTrack/me', json={'session_id': sessionID})
    assert response.status_code == 200 and json.loads(response.get_data().strip().decode("utf-8")) == me_data

    # Update admin account
    data["first_name"] = "Julian"
    data["last_name"] = "Ramos"
    data['session_id'] = sessionID

    response = client.put('classTrack/user/update/' + str(admin_id), json=data)
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode("utf-8"))['user_id'] == admin_id
    
    # Delete admin account
    response = client.post('classTrack/user/delete/' + str(admin_id), json=data)
    assert response.status_code == 200 and json.loads(
        response.get_data().strip().decode("utf-8"))['user_id'] == admin_id

def test_get_all_users(client):
    response = client.get('classTrack/users')
    assert response.status_code == 200

def test_logout_user(client, login_user):
    # Removing new lines from Session ID and decoding so it could be json compatible
    user_sessionID = login_user

    response = client.post('classTrack/logout',
                           json={"session_id": user_sessionID})
    assert response.status_code == 200 and response.get_data().strip().decode("utf-8").replace('"', "") == 'true'

# def test_get_admin_id(client):
#     response = client.get('classTrack/admin/71')
#     assert response.status_code == 200


# def test_create_user(client):

#     data = {
#         "isAdmin": False,
#         "variant_id": 4,
#         "first_name": "User test",
#         "last_name": "Account",
#         "email": "user@testaccount.com",
#         "password": "user"
#     }

#     response = client.post('classTrack/user', json=data)
#     assert response.status_code == 200


# def test_login_user(client):
#     response = client.post('classTrack/login', json=test_user)
#     assert response.status_code == 200





# def test_get_me(client, user_sessionID):
#     response = client.post(
#         'classTrack/me', json={"session_id": user_sessionID})
#     assert response.status_code == 200


# def test_get_student_by_id(client):
#     response = client.get('classTrack/student/70')
#     assert response.status_code == 200


# def test_get_admin_by_id(client):
#     response = client.get('classTrack/admin/61')
#     assert response.status_code == 200

# # Update


# def test_update_user_by_user(client, user_sessionID):
#     test_user = {
#         "isAdmin": False,
#         "variant_id": 4,
#         "first_name": "User test",
#         "last_name": "Account",
#         "email": "user@testaccount.com",
#         "password": "user"
#     }

#     response = client.put('classTrack/user/update/70',
#                           json=test_user, headers={'SessionID': user_sessionID})
#     assert response.status_code == 200


# def test_update_user_by_admin(client, admin_sessionID):
#     test_user = {
#         "isAdmin": False,
#         "variant_id": 4,
#         "first_name": "User test",
#         "last_name": "Account",
#         "email": "user@testaccount.com",
#         "password": "user"
#     }

#     response = client.put('classTrack/user/update/70',
#                           json=test_user, headers={'SessionID': admin_sessionID})
#     assert response.status_code == 200

# # Delete


# def test_delete_user_by_user(client, user_sessionID):
#     response = client.post('classTrack/user/delete/70',
#                            headers={"SessionID": user_sessionID})
#     assert response.status_code == 200


# def test_delete_user_by_admin(client, admin_sessionID):
#     response = client.post('classTrack/user/delete/70',
#                            headers={"SessionID": admin_sessionID})
#     assert response.status_code == 200
