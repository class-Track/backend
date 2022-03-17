from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.curriculums import Curriculums
from app.models.session_manager import SessionManager

SManager = SessionManager()
app_curriculum_routes = Blueprint('curriculums_routes', __name__)

# CREATE Curriculum
@app_curriculum_routes.route('/classTrack/curriculum', methods=['POST'])
def create_curriculum():
    s = SManager.get_tied_user(request.headers.get("SessionID"))
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    data = request.get_json()

    if s.user_id != data["user_id"]:
        return make_response(jsonify({"err": "Session and curriculum user_id mismatch"}), 403)

    curriculum_access = Curriculums()
    curriculum_id = curriculum_access.create(
        data["deptCode"], data["user_id"], data["department_id"])
    curriculum_access.close_connection()
    return make_response(jsonify(curriculum_id), 200)

# READ ALL
@app_curriculum_routes.route('/classTrack/curriculums', methods=['GET'])
def get_all_curriculums():
    curriculum_access = Curriculums()
    curriculums = curriculum_access.read_all()
    curriculum_access.close_connection()
    return make_response(jsonify(curriculums), 200)

# READ BY ID
@app_curriculum_routes.route('/classTrack/curriculum/<string:id>', methods=['GET'])
def get_curriculum(id):
    curriculum_access = Curriculums()
    curriculum = curriculum_access.read(id)
    curriculum_access.close_connection()
    if curriculum is None:
        return make_response(jsonify({"err": "Curriculum not found"}), 404)
    return make_response(jsonify(curriculum), 200)

# UPDATE
@app_curriculum_routes.route('/classTrack/curriculum/update/<string:id>', methods=['PUT'])
def update_curriculum(id):
    s = SManager.get_tied_user(request.headers.get("SessionID"))
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    data = request.get_json()
    curriculum_access = Curriculums()
    updated_curriculum = curriculum_access.update(
        id, data["rating"])
    curriculum_access.close_connection()
    return make_response(jsonify({"curriculum_id": updated_curriculum}), 200)

# DELETE
@app_curriculum_routes.route('/classTrack/curriculum/delete/<string:id>', methods=['POST'])
def delete_curriculum(id):
    s = SManager.get_tied_user(request.headers.get("SessionID"))
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    curriculum_access = Curriculums()

    c = curriculum_access.read(id)
    if c is None:
        curriculum_access.close_connection()
        return make_response(jsonify({"err": "Curriculum was not found"}), 404)

    if c.user_id != s.user_id:
        curriculum_access.close_connection()
        return make_response(jsonify({"err": "Session does not own curriculum"}), 403)

    deleted_curriculum = curriculum_access.delete(id)
    curriculum_access.close_connection()
    return make_response(jsonify({"curriculum_id": deleted_curriculum}), 200)
