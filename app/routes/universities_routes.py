from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.universities import Universities
from app.models.session_manager import SessionManager

SManager = SessionManager()
app_universities_routes = Blueprint('universities_routes', __name__)

# CREATE University
@app_universities_routes.route('/classTrack/university', methods=['POST'])
def create_university():
    data = request.get_json()
    s, _ = SManager.get_tied_user(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not False:  # If this is ever replaced by a role, replace this
        return make_response(jsonify({"err": "Insufficient Permissions"}), 403)

    university_access = Universities()
    university_id = university_access.create(
        data["name"], data["codification"], data["state"], data["country"])
    university_access.close_connection()
    return make_response(jsonify(university_id), 200)

# READ ALL
@app_universities_routes.route('/classTrack/universities', methods=['GET'])
def get_all_universities():
    university_access = Universities()
    universities = university_access.read_all()
    university_access.close_connection()
    return make_response(jsonify(universities), 200)

# READ BY ID
@app_universities_routes.route('/classTrack/university/<int:id>', methods=['GET'])
def get_university(id):
    university_access = Universities()
    university = university_access.read(id)
    university_access.close_connection()
    if university is None:
        return make_response(jsonify({"err": "University not found"}), 404)
    return make_response(jsonify(university), 200)

# UPDATE
@app_universities_routes.route('/classTrack/university/update/<int:id>', methods=['PUT'])
def update_university(id):
    data = request.get_json()
    s, admin = SManager.get_tied_student_or_admin(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    if not s['university_id'] == id:
        return make_response(jsonify({"err": "User does not administrate this university"}), 403)

    university_access = Universities()
    if university_access.read(id) is None:
        university_access.close_connection()
        return make_response(jsonify({"err": "University not found"}), 404)
    updated_university = university_access.update(
        id, data["name"], data["codification"], data["state"], data["country"])
    university_access.close_connection()
    return make_response(jsonify({"university_id": updated_university}), 200)        

# DELETE
@app_universities_routes.route('/classTrack/university/delete/<int:id>', methods=['POST'])
def delete_university(id):
    data = request.get_json()
    s, _ = SManager.get_tied_user(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not False:  # if this is ever replaced by a role, check it.
        return make_response(jsonify({"err": "Insufficient Permissions"}), 403)

    university_access = Universities()
    if university_access.read(id) is None:
        university_access.close_connection()
        return make_response(jsonify({"err": "University not found"}), 404)
    deleted_university = university_access.delete(id)
    university_access.close_connection()
    return make_response(jsonify({"university_id": deleted_university}), 200)        
