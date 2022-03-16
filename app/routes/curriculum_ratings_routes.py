from flask import Blueprint, request, make_response, Response
from flask.json import jsonify
from app.models.curriculum_ratings import Curriculum_Ratings

app_curriculum_ratings_routes = Blueprint('curriculum_ratings_routes', __name__)

# CREATE Degree
@app_curriculum_ratings_routes.route('/classTrack/curriculum_rating', methods=['POST'])
def create_curriculum_rating():
    data = request.get_json()
    curriculum_rating_access = Curriculum_Ratings()
    curriculum_rating_id = curriculum_rating_access.create(
        data["user_id"], data["curriculum_id"], data["rating"])
    curriculum_rating_access.close_connection()
    return make_response(jsonify(curriculum_rating_id), 200)

# READ ALL
@app_curriculum_ratings_routes.route('/classTrack/curriculum_ratings', methods=['GET'])
def get_all_curriculum_ratings():
    curriculum_rating_access = Curriculum_Ratings()
    curriculum_ratings = curriculum_rating_access.read_all()
    curriculum_rating_access.close_connection()
    return make_response(jsonify(curriculum_ratings), 200)

# READ BY ID
@app_curriculum_ratings_routes.route('/classTrack/curriculum_rating/<int:id>', methods=['GET'])
def get_curriculum_rating(id):
    curriculum_rating_access = Curriculum_Ratings()
    curriculum_rating = curriculum_rating_access.read(id)
    curriculum_rating_access.close_connection()
    if curriculum_rating is None:
        return make_response(jsonify({"err": "Curriculum rating not found"}), 404)
    return make_response(jsonify(curriculum_rating), 200)

# UPDATE
@app_curriculum_ratings_routes.route('/classTrack/curriculum_rating/update/<int:id>', methods=['PUT'])
def update_curriculum_rating(id):
    data = request.get_json()
    curriculum_rating_access = Curriculum_Ratings()
    updated_curriculum_rating = curriculum_rating_access.update(
        id, data["user_id"], data["curriculum_id"], data["rating"])
    curriculum_rating_access.close_connection()
    return make_response(jsonify({"rating_id": updated_curriculum_rating}), 200)

# DELETE
@app_curriculum_ratings_routes.route('/classTrack/curriculum_rating/delete/<int:id>', methods=['POST'])
def delete_curriculum_rating(id):
    curriculum_rating_access = Curriculum_Ratings()
    deleted_curriculum_rating = curriculum_rating_access.delete(id)
    curriculum_rating_access.close_connection()
    return make_response(jsonify({"rating_id": deleted_curriculum_rating}), 200)
