from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.categories import Categories
from app.models.session_manager import SessionManager

SManager = SessionManager()
app_categories_routes = Blueprint('categories_routes', __name__)

# CREATE Category
@app_categories_routes.route('/classTrack/category', methods=['POST'])
def create_category():
    data = request.get_json()
    s, admin = SManager.get_tied_student_or_admin(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    category_access = Categories()
    category_id = category_access.create(
        data["name"], data["classification"])
    return make_response(jsonify(category_id), 200)

# READ ALL
@app_categories_routes.route('/classTrack/categories', methods=['GET'])
def get_all_categories():
    category_access = Categories()
    categories = category_access.read_all()
    return make_response(jsonify(categories), 200)

# READ BY ID
@app_categories_routes.route('/classTrack/category/<int:id>', methods=['GET'])
def get_category(id):
    category_access = Categories()
    category = category_access.read(id)
    if category is None:
        return make_response(jsonify({"err": "Category not found"}), 404)
    return make_response(jsonify(category), 200)

# UPDATE
@app_categories_routes.route('/classTrack/category/update/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    s, admin = SManager.get_tied_student_or_admin(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    category_access = Categories()
    if category_access.read(id) is None:
        return make_response(jsonify({"err": "Category not found"}), 404)
    updated_category = category_access.update(
        id, data["name"], data["classification"])
    return make_response(jsonify({"category_id": updated_category}), 200)

# DELETE
@app_categories_routes.route('/classTrack/category/delete/<int:id>', methods=['POST'])
def delete_category(id):
    data = request.get_json()
    s, admin = SManager.get_tied_student_or_admin(data["session_id"])
    if s is None:
        return make_response(jsonify({"err": "Invalid Session"}), 401)

    if not admin:
        return make_response(jsonify({"err": "User is not an admin. They are a student"}), 403)

    category_access = Categories()
    c = category_access.read(id)
    if c is None:
        return make_response(jsonify({"err": "Category not found"}), 404)

    deleted_category = category_access.delete(id)
    return make_response(jsonify({"category_id": deleted_category}), 200)

