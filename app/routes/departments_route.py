from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.departments import Departments

app_departments_routes = Blueprint('departments_routes', __name__)

# CREATE Department
@app_departments_routes.route('/classTrack/department', methods=['POST'])
def create_department():
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
    data = request.get_json()
    department_access = Departments()
    updated_department = department_access.update(
        id, data["university_id"], data["name"], data["classification"])
    department_access.close_connection()
    return make_response(jsonify({"department_id": updated_department}), 200)

# DELETE
@app_departments_routes.route('/classTrack/department/delete/<int:id>', methods=['POST'])
def delete_department(id):
    department_access = Departments()
    deleted_department = department_access.delete(id)
    department_access.close_connection()
    return make_response(jsonify({"department_id": deleted_department}), 200)
