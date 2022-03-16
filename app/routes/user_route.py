from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.users import Users

app_users_routes = Blueprint('user_routes', __name__)

# CREATE User
@app_users_routes.route('/classTrack/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_access = Users()
    user_id = user_access.create(
        data["isAdmin"], data["variant_id"], data["first_name"], data["last_name"], data["email"], data["password"])
    user_access.close_connection()
    return make_response(jsonify(user_id), 200)

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
    user_access = Users()
    if user_access.readAdmin(id) is None and user_access.readStudent(id):
        user_access.close_connection()
        return make_response(jsonify({"err": "User not found"}), 404)
    deleted_user = user_access.delete(id)
    user_access.close_connection()
    return make_response(jsonify({"user_id": deleted_user}), 200)        
