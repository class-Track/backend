import pytest
from app.main import create_app

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

def test_get_all_curriculum_ratings(client):
    response = client.get('classTrack/curriculum_ratings')
    assert response.status_code == 200

# def test_get_curriculum_rating_by_id(client):
#     response = client.get('classTrack/curriculum_rating/1')
#     assert response.status_code == 200
