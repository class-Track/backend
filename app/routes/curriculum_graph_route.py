from flask import Blueprint, current_app, request, make_response, Response
from flask.json import jsonify
from app.models.curriculum_graph import CurruculumGraph
from app.models.session_manager import SessionManager

app_curr_graph_routes = Blueprint('curr_graph_routes', __name__, url_prefix="/classTrack")
SManager = SessionManager()

@app_curr_graph_routes.route('/standard_curriculum', methods=['POST'])
def create_standard_curriculum():
    data = request.get_json()
    dao = CurruculumGraph(current_app.driver)
    s, admin = SManager.get_tied_user(data["session_id"])

    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)
    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    curriculum = {    
        "id": data.pop('curriculum_sequence'),
        "name":  data.pop('name'),
        "program":  data.pop("deptCode"),
        "user": data.pop('user_id'),
        "length":  data.pop('length'),
        "credits":  data.pop('credits')
    }
    years = data.pop('year_list')['year_ids']

    categories_ids = data.pop('category_list')['category_ids'] if 'category_list' in data else None
    categories = [data[cat] for cat in categories_ids if cat in data] if categories_ids else None

    semesters_ids = [ s for y in years for s in data[y]['semester_ids']]
    semesters = [data[sem] for sem in semesters_ids]

    course_ids = data.pop('course_list')['course_ids']
    reqs = [data[co] for co in course_ids if (data[co]["prereqs"] or data[co]["coreqs"])]

    prereqs, coreqs = [],[]

    for c in reqs:
        for pre in c["prereqs"]:
            prereqs.append({"id": c["id"], "pre_id": pre["id"]})
        for co in c["coreqs"]:
            coreqs.append({"id": c["id"], "co_id": co["id"]})
        

    createdCurr = dao.create_standard_curr(curriculum, categories, semesters, prereqs, coreqs)

    
    return make_response(jsonify(createdCurr), 200)


@app_curr_graph_routes.route('/currGraph', methods=['GET'])
def get_curriculum():
    id = request.args.get("id")

    dao = CurruculumGraph(current_app.driver)

    curr = dao.get_curriculum(id)

    if not curr:
         return make_response(jsonify({"err": "Curriculum doesn't exist"}), 404)

    return make_response(jsonify(curr), 200)