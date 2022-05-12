from flask import Blueprint, current_app, request, make_response, Response
from flask.json import jsonify
from app.models.curriculums import Curriculums
from app.models.curriculum_graph import CurruculumGraph
from app.models.session_manager import SessionManager

SManager = SessionManager()
app_curriculum_routes = Blueprint('curriculums_routes', __name__)

# CREATE Curriculum
@app_curriculum_routes.route('/classTrack/custom_curriculum', methods=['POST'])
def create_curriculum():
    data = request.get_json()
    s, _ = SManager.get_tied_user(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)
    if str(s["user_id"]) != str(data["user_id"]):
        return make_response(jsonify({"err": "Session and curriculum user_id mismatch"}), 403)

    curriculum = {    
        "name":  data.pop('name'),
        "deptCode":  data.pop("deptCode"),
        "user_id": data.pop('user_id'),
        "length":  data.pop('length'),
        "credits":  data.pop('credits'),
        "degree_id": data.pop('degree_id'),
        "degree_name": data.pop('degree_name'),
        "department_id": data.pop('department_id'),
        "department_name": data.pop('department_name'),
        "isDraft": data.pop('isDraft')
    }
    years = data.pop('year_list')['year_ids']

    categories_ids = data.pop('category_list')['category_ids'] if ('category_list' in data and 'category_ids' in data['category_list']) else None
    categories = [data[cat] for cat in categories_ids if cat in data] if categories_ids else None

    semesters_ids = [ s for y in years for s in data[y]['semester_ids']]
    semesters = [data[sem] for sem in semesters_ids]

    course_ids = data.pop('course_list')['course_ids']
    cat_per_course =  [{"id": data[c]['course_id'], "category": data[c]['category']} for c in course_ids]

    curriculum_access = Curriculums()
    curriculum['curriculum_sequence'] = curriculum_access.create(curriculum.get("name"), curriculum.get("deptCode"), curriculum.get("user_id"), curriculum.get("degree_id"), len(semesters_ids), len(course_ids), curriculum['isDraft']).get("curriculum_id")

    dao = CurruculumGraph(current_app.driver)
    createdCurr = dao.create_custom_curr(curriculum, categories, semesters, cat_per_course)

    if(createdCurr is None):
        curriculum_access.delete(curriculum['curriculum_sequence'])
        return make_response(jsonify({"err": "Curriculum graph could not be created"}), 403)

    return make_response(jsonify({'id': curriculum['curriculum_sequence']}), 200)

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

# READ BY USER_ID
@app_curriculum_routes.route('/classTrack/curriculum/user/<string:id>', methods=['GET'])
def get_curriculum_by_user(id):
    curriculum_access = Curriculums()
    curriculum = curriculum_access.get_curriculum_by_user(id)
    if curriculum is None:
        return make_response(jsonify({"err": "User has no curriculums"}), 404)
    return make_response(jsonify(curriculum), 200)

# READ BY USER_ID
@app_curriculum_routes.route('/classTrack/curriculum/user_draft/<string:id>', methods=['GET'])
def get_drafts_by_user(id):
    curriculum_access = Curriculums()
    curriculum = curriculum_access.get_drafts_by_user(id)
    if curriculum is None:
        return make_response(jsonify({"err": "User has no curriculums"}), 404)
    return make_response(jsonify(curriculum), 200)

# READ TOP 9 BY DEGREE
@app_curriculum_routes.route('/classTrack/curriculum/top_degree', methods=['GET'])
def get_degree_most_visited():
    id = request.args.get("id")
    curriculum_access = Curriculums()
    curriculum = curriculum_access.get_degree_most_visited(id)
    if curriculum is None:
        return make_response(jsonify({"err": "There are no top curriculums"}), 404)
    return make_response(jsonify(curriculum), 200)

# READ TOP RATED 9 BY DEGREE
@app_curriculum_routes.route('/classTrack/curriculum/top_rated', methods=['GET'])
def get_degree_top_rated():
    id = request.args.get("id")
    curriculum_access = Curriculums()
    curriculum = curriculum_access.get_degree_top_rated(id)
    if curriculum is None:
        return make_response(jsonify({"err": "There are no top rated curriculums"}), 404)
    return make_response(jsonify(curriculum), 200)


# UPDATE
@app_curriculum_routes.route('/classTrack/curriculum/update_rating/<string:id>', methods=['PUT'])
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

# UPDATE 
@app_curriculum_routes.route('/classTrack/curriculum/update_custom', methods=['PUT'])
def update_custom_curriculum():
    data = request.get_json()
    s, _ = SManager.get_tied_user(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)
    if str(s["user_id"]) != str(data["user_id"]):
        return make_response(jsonify({"err": "Session and curriculum user_id mismatch"}), 403)

    curriculum = {    
        "name":  data.pop('name'),
        "deptCode":  data.pop("deptCode"),
        "user_id": data.pop('user_id'),
        "length":  data.pop('length'),
        "credits":  data.pop('credits'),
        "degree_id": data.pop('degree_id'),
        "degree_name": data.pop('degree_name'),
        "department_id": data.pop('department_id'),
        "department_name": data.pop('department_name'),
        "curriculum_sequence": data.pop('curriculum_sequence'),
        "isDraft": data.pop('isDraft')
    }
    years = data.pop('year_list')['year_ids']

    categories_ids = data.pop('category_list')['category_ids'] if ('category_list' in data and 'category_ids' in data['category_list']) else None
    categories = [data[cat] for cat in categories_ids if cat in data] if categories_ids else None

    semesters_ids = [ s for y in years for s in data[y]['semester_ids']]
    semesters = [data[sem] for sem in semesters_ids]

    course_ids = data.pop('course_list')['course_ids']
    cat_per_course =  [{"id": data[c]['course_id'], "category": data[c]['category']} for c in course_ids]

    curriculum_access = Curriculums()
    curriculum_access.update(curriculum['curriculum_sequence'], curriculum['name'],len(semesters_ids), len(course_ids), curriculum['isDraft'])

    dao = CurruculumGraph(current_app.driver)
    id = dao.update_custom_curriculum(curriculum['curriculum_sequence'], curriculum, categories, semesters, cat_per_course)

    return make_response(jsonify({"curriculum_id": id}), 200)

# DELETE
@app_curriculum_routes.route('/classTrack/curriculum/delete/<string:id>', methods=['POST'])
def delete_curriculum(id):
    data = request.get_json()
    s, admin = SManager.get_tied_user(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        curriculum_access = Curriculums()
        c = curriculum_access.read(id)
        if c is None:
            return make_response(jsonify({"err": "Curriculum was not found"}), 404)

        if c['user_id'] != s['user_id']:
            return make_response(jsonify({"err": "Session does not own curriculum"}), 403)
        curriculum_access.delete(id)
    
    deptCode = data['deptCode'] if data.get('deptCode') else None

    dao = CurruculumGraph(current_app.driver)
    wasDeleted = dao.delete_curriculum(id, deptCode)

    if(not wasDeleted):
        return make_response(jsonify({"err": "Curriculum was not deleted from graph db"}), 403)

    return make_response(jsonify({"curriculum_id": wasDeleted}), 200)
