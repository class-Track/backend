from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.departments import Departments
from app.SessionManager import SessionManager

SManager = SessionManager()
app_departments_routes = Blueprint('departments_routes', __name__)

# CREATE Department
@app_departments_routes.route('/classTrack/department', methods=['POST'])
def create_department():
    s, admin = SManager.get_tied_student_or_admin(request.headers.get("SessionID"))
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    data = request.get_json()

    if not s.university_id == data["university_id"]:
        return make_response(jsonify({"err": "User does not administrate this university"}), 403)

    department_access = Departments()
    department_id = department_access.create(
        data["university_id"], data["name"], data["classification"])
    department_access.close_connection()
    return make_response(jsonify(department_id), 200)

# READ ALL
@app_departments_routes.route('/classTrack/departments', methods=['GET'])
def get_all_departments():
    department_access = Departments()
    departments = department_access.read_all()
    department_access.close_connection()
    return make_response(jsonify(departments), 200)

# READ BY ID
@app_departments_routes.route('/classTrack/department/<int:id>', methods=['GET'])
def get_department(id):
    department_access = Departments()
    department = department_access.read(id)
    department_access.close_connection()
    if department is None:
        return make_response(jsonify({"err": "Department not found"}), 404)
    return make_response(jsonify(department), 200)

# UPDATE
@app_departments_routes.route('/classTrack/department/update/<int:id>', methods=['PUT'])
def update_department(id):
    s, admin = SManager.get_tied_student_or_admin(request.headers.get("SessionID"))
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    data = request.get_json()

    if not s.university_id == data["university_id"]:
        return make_response(jsonify({"err": "User does not administrate this university"}), 403)

    department_access = Departments()
    if department_access.read(id) is None:
        department_access.close_connection()
        return make_response(jsonify({"err": "Department not found"}), 404)
    updated_department = department_access.update(
        id, data["university_id"], data["name"], data["classification"])  # Allowing users to change the university of
    department_access.close_connection()                                  # a department can be detrimental, and pose
    return make_response(jsonify({"department_id": updated_department}), 200)  # A light security risk!

# DELETE
@app_departments_routes.route('/classTrack/department/delete/<int:id>', methods=['POST'])
def delete_department(id):
    s, admin = SManager.get_tied_student_or_admin(request.headers.get("SessionID"))
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an Admin, they are a Student"}), 403)

    department_access = Departments()

    d = department_access.read(id)

    if d is None:
        department_access.close_connection()
        return make_response(jsonify({"err": "Department not found"}), 404)

    if d.university_id != s.university_id:
        department_access.close_connection()
        return make_response(jsonify({"err": "User does not administrate this university"}), 404)

    deleted_department = department_access.delete(id)
    department_access.close_connection()
    return make_response(jsonify({"department_id": deleted_department}), 200)
