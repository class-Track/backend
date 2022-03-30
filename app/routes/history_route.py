from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.history import History
from app.models.session_manager import SessionManager

SManager = SessionManager()
app_history_routes = Blueprint('history_routes', __name__)

# CREATE History
@app_history_routes.route('/classTrack/history', methods=['POST'])
def create_history():
    data = request.get_json()
    s, _ = SManager.get_tied_user(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if s['user_id'] != data["user_id"]:
        return make_response(jsonify({"err": "Session and Data userID mismatch"}), 403)

    history_access = History()
    history_id = history_access.create(
        data["user_id"], data["curriculum_id"])
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
    # TODO Probably replace this with a way to get either top history items for someone or with a list of history
    # TODO for a specific person
    history_access = History()
    history = history_access.read(id)
    history_access.close_connection()
    if history is None:
        return make_response(jsonify({"err": "History not found"}), 404)
    return make_response(jsonify(history), 200)

# DELETE
@app_history_routes.route('/classTrack/history/delete/<int:id>', methods=['POST'])
def delete_history(id):
    data = request.get_json()
    s, admin = SManager.get_tied_student_or_admin(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    history_access = History()
    h = history_access.read(id)

    if h is None:
        history_access.close_connection()
        return make_response(jsonify({"err": "History not found"}), 404)

    if h['user_id'] != s['user_id'] and not admin:
        history_access.close_connection()
        return make_response(jsonify({"err": "Session does not own this history item"}), 403)

    deleted_history = history_access.delete(id)
    history_access.close_connection()
    return make_response(jsonify({"history_id": deleted_history}), 200)        
