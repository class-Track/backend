# import pytest
# from app.main import create_app

# # Global Variables
# test_user = {
#     "email": "test@testjulian.com",
#     "password": "test"
# }


# @pytest.fixture
# def app():
#     app = create_app()
#     app.config.update({
#         "TESTING": True,
#     })
#     yield app


# @pytest.fixture
# def client(app):
#     return app.test_client()


# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()


# @pytest.fixture
# def login(client):
#     # Login user to get SessionID
#     user = client.post('classTrack/login', json=test_user)
#     assert type(user.get_data()) == bytes

#     sessionID = user.get_data().strip().decode('utf-8').replace('"', "")

#     yield sessionID


# def test_create_curriculum_rating(client, sessionID):
#     # Curriculum rating
#     rating = {
#         'user_id': 70,
#         'curriculum_id': 'CIIC_57_V1',
#         'rating': 4
#     }

#     response = client.post('classTrack/curriculum_rating',
#                            json=rating, headers={'SessionID': sessionID})
#     assert response.status_code == 200


# def test_get_all_curriculum_ratings(client):
#     response = client.get('classTrack/curriculum_ratings')
#     assert response.status_code == 200


# def test_get_curriculum_rating_by_id(client):
#     response = client.get('classTrack/curriculum_rating/3')
#     assert response.status_code == 200


# def test_update_curriculum_rating(client, sessionID):
#     rating = {
#         'user_id': 70,
#         'curriculum_id': 'CIIC_57_V1',
#         'rating': 3
#     }

#     response = client.put('classTrack/curriculum_rating/update/3',
#                           json=rating, headers={'SessionID': sessionID})
#     assert response.status_code == 200

# def test_delete_curriculum_rating(client, sessionID):
#     response = client.post('classTrack/curriculum_rating/delete/10')
#     assert response.status_code == 200
