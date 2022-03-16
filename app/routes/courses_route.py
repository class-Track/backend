from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.courses import Courses

app_course_routes = Blueprint('courses_routes', __name__)

# CREATE Course
@app_course_routes.route('/classTrack/course', methods=['POST'])
def create_course():
    data = request.get_json()
    course_access = Courses()
    course_id = course_access.create(
        data["department_id"], data["name"], data["classification"])
    course_access.close_connection()
    return make_response(jsonify(course_id), 200)

# READ ALL
@app_course_routes.route('/classTrack/courses', methods=['GET'])
def get_all_courses():
    course_access = Courses()
    courses = course_access.read_all()
    course_access.close_connection()
    return make_response(jsonify(courses), 200)

# READ BY ID
@app_course_routes.route('/classTrack/course/<int:id>', methods=['GET'])
def get_course(id):
    course_access = Courses()
    course = course_access.read(id)
    course_access.close_connection()
    if course is None:
        return make_response(jsonify({"err": "Course not found"}), 404)
    return make_response(jsonify(course), 200)

# UPDATE
@app_course_routes.route('/classTrack/course/update/<int:id>', methods=['PUT'])
def update_course(id):
    data = request.get_json()
    course_access = Courses()
    if course_access.read(id) is None:
        course_access.close_connection()
        return make_response(jsonify({"err": "Course not found"}), 404)
    updated_course = course_access.update(
        id, data["department_id"], data["name"], data["classification"])
    course_access.close_connection()
    return make_response(jsonify({"course_id": updated_course}), 200)

# DELETE
@app_course_routes.route('/classTrack/course/delete/<int:id>', methods=['POST'])
def delete_course(id):
    course_access = Courses()
    if course_access.read(id) is None:
        course_access.close_connection()
        return make_response(jsonify({"err": "Course not found"}), 404)
    deleted_course = course_access.delete(id)
    course_access.close_connection()
    return make_response(jsonify({"course_id": deleted_course}), 200)
