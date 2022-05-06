from flask import Blueprint, request, current_app, make_response, Response
from flask.json import jsonify
from app.models.courses import Courses
from app.models.departments import Departments
from app.models.session_manager import SessionManager
from app.models.curriculum_graph import CurruculumGraph

SManager = SessionManager()
app_course_routes = Blueprint('courses_routes', __name__, url_prefix="/classTrack")

# CREATE Course
@app_course_routes.route('/course', methods=['POST'])
def create_course():
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

    course_access = Courses()
    course_id = course_access.create(
        data["department_id"], data["name"], data["classification"])
    return make_response(jsonify(course_id), 200)

# READ ALL
@app_course_routes.route('/courses', methods=['GET'])
def get_all_courses():
    course_access = Courses()
    courses = course_access.read_all()
    return make_response(jsonify(courses), 200)

# READ BY ID
@app_course_routes.route('/course/<int:id>', methods=['GET'])
def get_course(id):
    course_access = Courses()
    course = course_access.read(id)
    if course is None:
        return make_response(jsonify({"err": "Course not found"}), 404)
    return make_response(jsonify(course), 200)

# UPDATE
@app_course_routes.route('/course/update/<int:id>', methods=['PUT'])
def update_course(id):
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

    course_access = Courses()
    if course_access.read(id) is None:
        return make_response(jsonify({"err": "Course not found"}), 404)
    updated_course = course_access.update(
        id, data["department_id"], data["name"], data["classification"])
    return make_response(jsonify({"course_id": updated_course}), 200)

# DELETE
@app_course_routes.route('/course/delete/<int:id>', methods=['POST'])
def delete_course(id):
    data = request.get_json()
    s, admin = SManager.get_tied_student_or_admin(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    course_access = Courses()
    c = course_access.read(id)
    if c is None:
        return make_response(jsonify({"err": "Course not found"}), 404)

    # We can assume the department for this degree exists as its a foreign key
    if __get_department__(c['department_id'])['university_id'] != s['university_id']:
        return make_response(jsonify({"err": "University is not administered by this user"}), 404)

    deleted_course = course_access.delete(id)
    return make_response(jsonify({"course_id": deleted_course}), 200)


def __get_department__(id):  # TODO: Eventually remove this
    departments_access = Departments()
    d = departments_access.read(id)
    return d


@app_course_routes.route('/course/prereqs', methods=['GET'])
def get_pre_reqs():
    id = request.args.get("id")

    dao = CurruculumGraph(current_app.driver)
    curr = dao.get_pre_reqs(id)

    if not curr:
         return make_response(jsonify({"err": "Course doesn't exist"}), 404)

    return make_response(jsonify(curr), 200)

@app_course_routes.route('/course/coreqs', methods=['GET'])
def get_co_reqs():
    id = request.args.get("id")

    dao = CurruculumGraph(current_app.driver)
    curr = dao.get_co_reqs(id)

    if not curr:
         return make_response(jsonify({"err": "Course doesn't exist"}), 404)

    return make_response(jsonify(curr), 200)
