from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.departments import Departments
from app.SessionManager import SessionManager

SManager = SessionManager()
app_departments_routes = Blueprint('departments_routes', __name__)

# CREATE Department
@app_departments_routes.route('/classTrack/department', methods=['POST'])
def create_department():
    s = SManager.get_tied_user(request.headers.get("SessionID"))
    if s is None:
        return make_response("Invalid Session", 401)

    if not False:  # TODO Check for admin role and/or check if this is one of the university's admin
        return make_response("Insufficient permissions", 403)

    data = request.get_json()
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
    s = SManager.get_tied_user(request.headers.get("SessionID"))
    if s is None:
        return make_response("Invalid Session", 401)

    if not False:  # TODO Check for admin role and/or check if this is one of the university's admin
        return make_response("Insufficient permissions", 403)

    data = request.get_json()
    department_access = Departments()
    if department_access.read(id) is None:
        department_access.close_connection()
        return make_response(jsonify({"err": "Department not found"}), 404)
    updated_department = department_access.update(
        id, data["university_id"], data["name"], data["classification"])
    department_access.close_connection()
    return make_response(jsonify({"department_id": updated_department}), 200)

# DELETE
@app_departments_routes.route('/classTrack/department/delete/<int:id>', methods=['POST'])
def delete_department(id):
    s = SManager.get_tied_user(request.headers.get("SessionID"))
    if s is None:
        return make_response("Invalid Session", 401)

    if not False:  # TODO Check for admin role and/or check if this is one of the university's admin
        return make_response("Insufficient permissions", 403)

    department_access = Departments()
    if department_access.read(id) is None:
        department_access.close_connection()
        return make_response(jsonify({"err": "Department not found"}), 404)
    deleted_department = department_access.delete(id)
    department_access.close_connection()
    return make_response(jsonify({"department_id": deleted_department}), 200)
