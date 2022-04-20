from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.curriculums import Curriculums
from app.models.session_manager import SessionManager

SManager = SessionManager()
app_curriculum_routes = Blueprint('curriculums_routes', __name__)

# CREATE Curriculum
@app_curriculum_routes.route('/classTrack/curriculum', methods=['POST'])
def create_curriculum():
    data = request.get_json()
    s, _ = SManager.get_tied_user(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if s["user_id"] != data["user_id"]:
        return make_response(jsonify({"err": "Session and curriculum user_id mismatch"}), 403)

    curriculum_access = Curriculums()
    curriculum_id = curriculum_access.create(
        data["name"], data["deptCode"], data["user_id"], data["department_id"])
    return make_response(jsonify(curriculum_id), 200)

# READ ALL
@app_curriculum_routes.route('/classTrack/curriculums', methods=['GET'])
def get_all_curriculums():
    curriculum_access = Curriculums()
    curriculums = curriculum_access.read_all()
    return make_response(jsonify(curriculums), 200)

# READ BY ID
@app_curriculum_routes.route('/classTrack/curriculum/<string:id>', methods=['GET'])
def get_curriculum(id):
    curriculum_access = Curriculums()
    curriculum = curriculum_access.read(id)
    if curriculum is None:
        return make_response(jsonify({"err": "Curriculum not found"}), 404)
    return make_response(jsonify(curriculum), 200)

# UPDATE
@app_curriculum_routes.route('/classTrack/curriculum/update/<string:id>', methods=['PUT'])
def update_curriculum_rating(id):
    data = request.get_json()
    s, _ = SManager.get_tied_user(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    curriculum_access = Curriculums()
    updated_curriculum = curriculum_access.update_rating(
        id, data["rating"])
    return make_response(jsonify({"curriculum_id": updated_curriculum}), 200)

# Rename 
@app_curriculum_routes.route('/classTrack/curriculum/rename/<string:id>', methods=['PUT'])
def rename_curriculum(id):
    data = request.get_json()
    s, _ = SManager.get_tied_user(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    curriculum_access = Curriculums()
    updated_curriculum = curriculum_access.rename(
        id, data["name"])
    return make_response(jsonify({"curriculum_id": updated_curriculum}), 200)

# DELETE
@app_curriculum_routes.route('/classTrack/curriculum/delete/<string:id>', methods=['POST'])
def delete_curriculum(id):
    data = request.get_json()
    s, _ = SManager.get_tied_user(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    curriculum_access = Curriculums()

    c = curriculum_access.read(id)
    if c is None:
        return make_response(jsonify({"err": "Curriculum was not found"}), 404)

    if c['user_id'] != s['user_id']:
        return make_response(jsonify({"err": "Session does not own curriculum"}), 403)

    deleted_curriculum = curriculum_access.delete(id)
    return make_response(jsonify({"curriculum_id": deleted_curriculum}), 200)
