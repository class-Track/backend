import pytest 
from flask import Flask

@pytest.fixture()
def app():
    app = Flask(__name__)

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner() 

def test_hello(client):
    response = client.get('/')
    assert response.get_data() == 'Hello, Class Track!'
        

