from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

class Curriculum_Ratings:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='ec2-34-231-183-74.compute-1.amazonaws.com',
            database='ddetn88o84e93n',
            user='oisewifxugdivf',
            password='155a4e05bef9407085766f6326277a143b1aa857ed8210c48a4f4517947dd563'
        )

    def create(self, user_id, curriculum_id, rating):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO curriculum_ratings (user_id, curriculum_id, rating)"
                " VALUES ( %(user_id)s, %(curriculum_id)s, %(rating)s )"
                " RETURNING rating_id", {
                    "user_id": user_id, "curriculum_id": curriculum_id, "rating": rating}
            )
            self.connection.commit()
            rating_id = cursor.fetchone()
            return rating_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT user_id, curriculum_id, rating FROM curriculum_ratings")
            self.connection.commit()
            curriculum_ratings = cursor.fetchall()
            return curriculum_ratings

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT user_id, curriculum_id, rating FROM curriculum_ratings WHERE rating_id=%(rating_id)s",
                           {"rating_id": id})
            self.connection.commit()
            try:
                rating = cursor.fetchone()
            except TypeError:
                rating = None
            return rating

    def update(self, id, rating):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE curriculum_ratings"
                " SET rating=%(rating)s"
                " WHERE rating_id=%(rating_id)s ",
                {"rating_id": id, "rating": rating})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM curriculum_ratings WHERE rating_id=%(rating_id)s", {"rating_id": id})
            self.connection.commit()
            return id

    # Clean-Up
    def close_connection(self):
        self.connection.close()
