from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.degrees import Degrees

app_degrees_routes = Blueprint('degrees_routes', __name__)

# CREATE Degree
@app_degrees_routes.route('/classTrack/degree', methods=['POST'])
def create_degree():
    data = request.get_json()
    degree_access = Degrees()
    degree_id = degree_access.create(
        data["department_id"], data["curriculum_sequence"], data["length"], data["credits"])
    degree_access.close_connection()
    return make_response(jsonify(degree_id), 200)

# READ ALL
@app_degrees_routes.route('/classTrack/degrees', methods=['GET'])
def get_all_degrees():
    degree_access = Degrees()
    degrees = degree_access.read_all()
    degree_access.close_connection()
    return make_response(jsonify(degrees), 200)

# READ BY ID
@app_degrees_routes.route('/classTrack/degree/<int:id>', methods=['GET'])
def get_degree(id):
    degree_access = Degrees()
    degree = degree_access.read(id)
    degree_access.close_connection()
    if degree is None:
        return make_response(jsonify({"err": "Degree not found"}), 404)
    return make_response(jsonify(degree), 200)

# UPDATE
@app_degrees_routes.route('/classTrack/degree/update/<int:id>', methods=['PUT'])
def update_degree(id):
    data = request.get_json()
    degree_access = Degrees()
    updated_degree = degree_access.update(
        id, data["name"], data["codification"], data["state"], data["\country"])
    degree_access.close_connection()
    return make_response(jsonify({"degree_id": updated_degree}), 200)

# DELETE
@app_degrees_routes.route('/classTrack/degree/delete/<int:id>', methods=['POST'])
def delete_degree(id):
    degree_access = Degrees()
    deleted_degree = degree_access.delete(id)
    degree_access.close_connection()
    return make_response(jsonify({"degree_id": deleted_degree}), 200)
