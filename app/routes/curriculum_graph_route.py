from flask import Blueprint, current_app, request, make_response, Response
from flask.json import jsonify
from app.models.curriculum_graph import CurruculumGraph
from app.models.session_manager import SessionManager

app_curr_graph__routes = Blueprint('curr_graph__routes', __name__, url_prefix="/classTrack/currGraph")

@app_curr_graph__routes.route('', methods=['POST'])
def create_route():
    data = request.get_json()

    id = data['id']
    graph = data['graph']

    dao = CurruculumGraph(current_app.driver)

    curr = dao.create_curr(id, graph)

    return jsonify(curr)