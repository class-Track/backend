from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.universities import Universities

app_university_routes = Blueprint('universities_routes', __name__)

# CREATE University
@app_university_routes.route('/classTrack/university', methods=['POST'])
def create_university():
    data = request.get_json()
    university_access = Universities()
    university_id = university_access.create(
        data["name"], data["codification"], data["state"], data["country"])
    university_access.close_connection()
    return make_response(jsonify(university_id), 200)

# READ ALL
@app_university_routes.route('/classTrack/universities', methods=['GET'])
def get_all_universities():
    university_access = Universities()
    universities = university_access.read_all()
    university_access.close_connection()
    return make_response(jsonify(universities), 200)

# READ BY ID
@app_university_routes.route('/classTrack/university/<int:id>', methods=['GET'])
def get_university(id):
    university_access = Universities()
    university = university_access.read(id)
    university_access.close_connection()
    if university is None:
        return make_response(jsonify({"err": "University not found"}), 404)
    return make_response(jsonify(university), 200)

# UPDATE
@app_university_routes.route('/classTrack/university/update/<int:id>', methods=['PUT'])
def update_university(id):
    data = request.get_json()
    university_access = Universities()
    updated_university = university_access.update(
        id, data["name"], data["codification"], data["state"], data["country"])
    university_access.close_connection()
    return make_response(jsonify({"university_id": updated_university}), 200)

# DELETE
@app_university_routes.route('/classTrack/university/delete/<int:id>', methods=['POST'])
def delete_university(id):
    university_access = Universities()
    deleted_university = university_access.delete(id)
    university_access.close_connection()
    return make_response(jsonify({"university_id": deleted_university}), 200)
