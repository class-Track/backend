from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.users import Users
from app.models.session_manager import SessionManager

SManager = SessionManager()
app_users_routes = Blueprint('user_routes', __name__)

# CREATE - User (SignUp)
@app_users_routes.route('/classTrack/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_access = Users()
    user_id = user_access.signUp(
        data["isAdmin"], data["variant_id"], data["first_name"], data["last_name"], data["email"], data["password"])
    user_access.close_connection()
    if not user_id:
        return make_response(jsonify({"err": "There exists an account with this email"}), 400)
    return make_response(jsonify(user_id), 200)

@app_users_routes.route('/classTrack/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user_access = Users()
    user = user_access.login(
        data["email"], data["password"])
    user_access.close_connection()
    if user is None:
        return make_response(jsonify({"err": "Email or Password not found"}), 404)

    session = SManager.login(user['user_id'])
    return make_response(jsonify(session), 200)  # Upon login we don't return user. We return a session

@app_users_routes.route('/classTrack/logout', methods=['POST'])
def logout_user():
    data = request.get_json()
    removed_session = SManager.logout(data["session_id"])

    if removed_session is None:  # This is technically not necessary. I only add this check because I don't want to make
        return make_response(jsonify({"err": "Session was not found"}, 404))  # Jsonify flip because it received None

    return make_response(jsonify(removed_session), 200)

# Get associated student/admin
@app_users_routes.route('/classTrack/me', methods=['POST'])
def get_me():
    data = request.get_json()
    s, admin = SManager.get_tied_student_or_admin(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    s["isAdmin"] = admin
    return make_response(jsonify(s), 200)

# READ ALL
@app_users_routes.route('/classTrack/users', methods=['GET'])
def get_all_users():
    user_access = Users()
    users = user_access.read_all()
    user_access.close_connection()
    return make_response(jsonify(users), 200)

# READ Student BY ID
@app_users_routes.route('/classTrack/student/<int:id>', methods=['GET'])
def get_student(id):
    user_access = Users()
    user = user_access.readStudent(id)
    user_access.close_connection()
    if user is None:
        return make_response(jsonify({"err": "User not found"}), 404)
    return make_response(jsonify(user), 200)

# READ Admin BY ID
@app_users_routes.route('/classTrack/admin/<int:id>', methods=['GET'])
def get_admin(id):
    user_access = Users()
    user = user_access.readAdmin(id)
    user_access.close_connection()
    if user is None:
        return make_response(jsonify({"err": "User not found"}), 404)
    return make_response(jsonify(user), 200)

# UPDATE
@app_users_routes.route('/classTrack/user/update/<int:id>', methods=['PUT'])
def update_user(id):

    s, admin = SManager.get_tied_student_or_admin(request.headers.get("SessionID"))
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if s.user_id() != id and not admin:
        return make_response(jsonify({"err": "Session is not tied to this user"}), 403)

    data = request.get_json()
    user_access = Users()
    if user_access.readAdmin(id) is None and user_access.readStudent(id):
        user_access.close_connection()
        return make_response(jsonify({"err": "User not found"}), 404)
    updated_user = user_access.update(
        id, data["isAdmin"], data["variant_id"], data["first_name"], data["last_name"], data["email"], data["password"])
    user_access.close_connection()
    return make_response(jsonify({"user_id": updated_user}), 200)

# DELETE
@app_users_routes.route('/classTrack/user/delete/<int:id>', methods=['POST'])
def delete_user(id):
    s, admin = SManager.get_tied_student_or_admin(request.headers.get("SessionID"))
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if s.user_id != id and not admin:  # honestly I cannot believe this uses "and" and "not" instead of && and !
        return make_response(jsonify({"err": "Session is not tied to this user"}), 403)

    user_access = Users()
    if user_access.readAdmin(id) is None and user_access.readStudent(id):
        user_access.close_connection()
        return make_response(jsonify({"err": "User not found"}), 404)
    deleted_user = user_access.delete(id)
    user_access.close_connection()
    return make_response(jsonify({"user_id": deleted_user}), 200)        
