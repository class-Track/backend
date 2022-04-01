# import pytest
# from app.main import create_app
# import psycopg2

# # Global Variables
# test_user = {
#     "email": "test@testjulian.com",
#     "password": "test"
# }
# test_admin = {
#     "email": "admin@account.com",
#     "password": "admin"
# }


# @pytest.fixture
# def app():
#     app = create_app()
#     app.config["TESTING"] = True
#     app.testing = True
#     yield app


# @pytest.fixture
# def client(app):
#     return app.test_client()


# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()


# @pytest.fixture
# def login_user(client):
#     login = client.post('classTrack/login', json=test_user)
#     assert type(login.get_data()) == bytes

#     # Removing new lines from Session ID and decoding so it could be json compatible
#     user_sessionID = login.get_data().strip().decode("utf-8").replace('"', "")

#     yield user_sessionID


# @pytest.fixture
# def login_admin(client):
#     login = client.post('classTrack/login', json=test_admin)
#     assert type(login.get_data()) == bytes

#     # Removing new lines from Session ID and decoding so it could be json compatible
#     admin_sessionID = login.get_data().strip().decode("utf-8").replace('"', "")

#     yield admin_sessionID


# def test_create_admin(client):

#     data = {
#         "isAdmin": True,
#         "variant_id": 2,
#         "first_name": "Admin test",
#         "last_name": "Account 1",
#         "email": "admin1@account.com",
#         "password": "admin"
#     }

#     response = client.post('classTrack/user', json=data)
#     assert response.status_code == 200


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


# def test_logout_user(client, user_sessionID):
#     response = client.post('classTrack/logout',
#                            json={"session_id": user_sessionID})
#     assert response.status_code == 200


# def test_get_me(client, user_sessionID):
#     response = client.post(
#         'classTrack/me', json={"session_id": user_sessionID})
#     assert response.status_code == 200


# def test_get_all_users(client):
#     response = client.get('classTrack/users')
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
