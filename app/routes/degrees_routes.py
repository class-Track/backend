from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.degrees import Degrees
from app.models.departments import Departments
from app.models.session_manager import SessionManager

SManager = SessionManager()
app_degrees_routes = Blueprint('degrees_routes', __name__)

# CREATE Degree
@app_degrees_routes.route('/classTrack/degree', methods=['POST'])
def create_degree():
    data = request.get_json()
    s, admin = SManager.get_tied_student_or_admin(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    d = __get_department__(data["department_id"])  # We should probably have checked if the department we were trying to
                                                   # add this degree to existed to begin with.
    if d is None:
        return make_response(jsonify({"err": "Department not found"}), 404)

    if d['university_id'] != s['university_id']:
        return make_response(jsonify({"err": "University is not administered by this user"}), 404)

    degree_access = Degrees()
    degree_id = degree_access.create(
       data["name"], data["department_id"], data["curriculum_sequence"], data["length"], data["credits"])
    degree_access.close_connection()
    return make_response(jsonify(degree_id), 200)

# READ ALL
@app_degrees_routes.route('/classTrack/degrees', methods=['GET'])
def get_all_degrees():
    degree_access = Degrees()
    degrees = degree_access.read_all()
    degree_access.close_connection()
    return make_response(jsonify(degrees), 200)

# READ ALL
@app_degrees_routes.route('/classTrack/degrees_dept', methods=['GET'])
def get_all_degrees_with_dept():
    degree_access = Degrees()
    degrees = degree_access.read_all_with_dept()
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
    s, admin = SManager.get_tied_student_or_admin(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    d = __get_department__(data["department_id"])

    if d is None:
        return make_response(jsonify({"err": "Department not found"}), 404)

    if d['university_id'] != s['university_id']:
        return make_response(jsonify({"err": "University is not administered by this user"}), 404)

    degree_access = Degrees()
    if degree_access.read(id) is None:
        degree_access.close_connection()
        return make_response(jsonify({"err": "Degree not found"}), 404)
    updated_degree = degree_access.update(
        id, data["name"], data["department_id"], data["curriculum_sequence"], data["length"], data["credits"])
    degree_access.close_connection()
    return make_response(jsonify({"degree_id": updated_degree}), 200)

# DELETE
@app_degrees_routes.route('/classTrack/degree/delete/<int:id>', methods=['POST'])
def delete_degree(id):
    s, admin = SManager.get_tied_student_or_admin(request.headers.get("SessionID"))
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    degree_access = Degrees()

    deg = degree_access.read(id)

    if deg is None:
        degree_access.close_connection()
        return make_response(jsonify({"err": "Degree not found"}), 404)

    # We can assume the department for this degree exists as its a foreign key
    if __get_department__(deg.department_id).university_id != s.university_id:
        degree_access.close_connection()
        return make_response(jsonify({"err": "University is not administered by this user"}), 404)

    deleted_degree = degree_access.delete(id)
    degree_access.close_connection()
    return make_response(jsonify({"degree_id": deleted_degree}), 200)


def __get_department__(id):  # TODO: Eventually remove this
    departments_access = Departments()
    d = departments_access.read(id)
    departments_access.close_connection()
    return d
