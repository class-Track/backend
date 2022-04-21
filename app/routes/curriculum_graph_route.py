from flask import Blueprint, current_app, request, make_response, Response
from flask.json import jsonify
from app.models.curriculum_graph import CurruculumGraph
from app.models.session_manager import SessionManager

app_curr_graph_routes = Blueprint('curr_graph_routes', __name__, url_prefix="/classTrack/currGraph")

@app_curr_graph_routes.route('/admin', methods=['POST'])
def create_standard_curriculum():
    data = request.get_json()

    graph = data['graph']
    co_reqs = data['co_reqs']
    pre_reqs = data['pre_reqs']

    dao = CurruculumGraph(current_app.driver)

    curr = dao.create_standard_curr(graph, co_reqs, pre_reqs)

    return jsonify(curr)

@app_curr_graph_routes.route('/student', methods=['POST'])
def create_custom_curriculum():
    data = request.get_json()

    graph = data['graph']

    dao = CurruculumGraph(current_app.driver)

    curr = dao.create_custom_curr(graph)

    return jsonify(curr)


@app_curr_graph_routes.route('/curr', methods=['GET'])
def get_curriculum():
    data = request.get_json()

    currName = data['name']

    dao = CurruculumGraph(current_app.driver)

    curr = dao.get_curriculum(currName)

    return jsonify(curr)