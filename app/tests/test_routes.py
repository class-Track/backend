from flask import Flask
from backend.app.routes.courses_route import courses_route
import json


def  test_create_course():
    app = Flask(__name__)
    courses_route(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.get_data() == b'Hello, Class Track!'
    assert response.status_code == 200
