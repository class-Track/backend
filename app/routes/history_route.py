from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.history import History

app_history_routes = Blueprint('history_routes', __name__)

# CREATE History
@app_history_routes.route('/classTrack/history', methods=['POST'])
def create_history():
    data = request.get_json()
    history_access = History()
    history_id = history_access.create(
        data["name"], data["codification"], data["state"], data["country"])
    history_access.close_connection()
    return make_response(jsonify(history_id), 200)

# READ ALL
@app_history_routes.route('/classTrack/history', methods=['GET'])
def get_all_histories():
    history_access = History()
    history = history_access.read_all()
    history_access.close_connection()
    return make_response(jsonify(history), 200)

# READ BY ID
@app_history_routes.route('/classTrack/history/<int:id>', methods=['GET'])
def get_history(id):
    history_access = History()
    history = history_access.read(id)
    history_access.close_connection()
    if history is None:
        return make_response(jsonify({"err": "History not found"}), 404)
    return make_response(jsonify(history), 200)

# UPDATE
@app_history_routes.route('/classTrack/history/update/<int:id>', methods=['PUT'])
def update_history(id):
    data = request.get_json()
    history_access = History()
    if history_access.read(id) is None:
        history_access.close_connection()
        return make_response(jsonify({"err": "History not found"}), 404)
    updated_history = history_access.update(
        id, data["name"], data["codification"], data["state"], data["country"])
    history_access.close_connection()
    return make_response(jsonify({"history_id": updated_history}), 200)

# DELETE
@app_history_routes.route('/classTrack/history/delete/<int:id>', methods=['POST'])
def delete_history(id):
    history_access = History()
    if history_access.read(id) is None:
        history_access.close_connection()
        return make_response(jsonify({"err": "History not found"}), 404)
    deleted_history = history_access.delete(id)
    history_access.close_connection()
    return make_response(jsonify({"history_id": deleted_history}), 200)        
