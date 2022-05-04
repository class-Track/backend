from dotenv import load_dotenv
from flask import make_response
from flask.json import jsonify
from psycopg2.extras import RealDictCursor

from app.dbconnection import dbconnection

load_dotenv()

class Curriculums:
    def __init__(self):
        self.connection = dbconnection().connection()

    def create(self, name, deptCode, user_id, degree_id, semesters, course_count):
        curriculum = '{}_{}'.format(deptCode, user_id)
        
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT count(curriculum_id) as curr_count FROM curriculums" 
                " WHERE curriculum_id LIKE '%{}%' ".format(curriculum)
            )
            self.connection.commit()
            count = cursor.fetchone()['curr_count']

            curriculum_id = '{}_V{}'.format(curriculum, count+1)

            cursor.execute(
                "INSERT INTO curriculums (name, curriculum_id, user_id, degree_id, rating, semesters, course_count)"
                " VALUES ( %(name)s, %(curriculum_id)s, %(user_id)s, %(degree_id)s, 0, %(semesters)s, %(course_count)s)"
                " RETURNING curriculum_id", {
                    "name": name, "curriculum_id": curriculum_id, "user_id": user_id, "degree_id": degree_id, "rating": 0, "semesters":semesters, "course_count":course_count }
            )
            self.connection.commit()
            curriculum_id = cursor.fetchone()
            return curriculum_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT name, curriculum_id, user_id, degree_id, rating, semesters, course_count FROM curriculums")
            self.connection.commit()
            curriculums = cursor.fetchall()
            return curriculums

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT name, curriculum_id, user_id, degree_id, rating, semesters, course_count FROM curriculums WHERE curriculum_id=%(curriculum_id)s",
                           {"curriculum_id": id})
            self.connection.commit()
            try:
                curriculum = cursor.fetchone()
            except TypeError:
                curriculum = None
            return curriculum
    
    def get_curriculum_by_user(self, user_id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                            SELECT  cu.curriculum_id, cu.name, cu.rating, de.name AS degree_name, de.length AS years, de.credits, cu.semesters, cu.course_count FROM curriculums cu
                            INNER JOIN degrees de ON de.degree_id = cu.degree_id
                            INNER JOIN departments d ON de.department_id = d.department_id
                            INNER JOIN users u ON u.user_id = cu.user_id
                            WHERE cu.user_id = %(user_id)s
                            GROUP BY cu.curriculum_id, cu.name, de.credits, de.name, cu.rating, de.length, cu.semesters, cu.course_count""",
                            {"user_id":user_id}
            )
            self.connection.commit()
            try:
                curriculums = cursor.fetchall()
            except TypeError:
                curriculums = None
            return curriculums

    def get_degree_most_visited(self, degree_id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                            SELECT  h.curriculum_id, cu.name, cu.rating, concat(first_name,' ',last_name) AS user, de.name AS degree_name, de.length AS years, de.credits, cu.semesters, cu.course_count, COUNT(*) AS times_visited FROM history h
                            INNER JOIN curriculums cu on cu.curriculum_id = h.curriculum_id
                            INNER JOIN degrees de ON de.degree_id = cu.degree_id
                            INNER JOIN departments d ON de.department_id = d.department_id
                            INNER JOIN users u ON u.user_id = cu.user_id
                            WHERE de.degree_id = %(degree_id)s
                            GROUP BY h.curriculum_id, cu.name, de.credits, u.first_name, u.last_name, de.name, cu.rating, de.length, cu.semesters, cu.course_count
                            ORDER BY times_visited DESC
                            LIMIT 9;
                            """,
                            {"degree_id":degree_id}
            )
            self.connection.commit()
            try:
                curriculums = cursor.fetchall()
            except TypeError:
                curriculums = None
            return curriculums

    def get_degree_top_rated(self, degree_id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                            SELECT  cu.curriculum_id, cu.name, cu.rating, concat(first_name,' ',last_name) AS user, de.name AS degree_name, de.length AS years, de.credits, cu.semesters, cu.course_count FROM curriculums cu
                            INNER JOIN degrees de ON de.degree_id = cu.degree_id
                            INNER JOIN departments d ON de.department_id = d.department_id
                            INNER JOIN users u ON u.user_id = cu.user_id
                            WHERE de.degree_id = %(degree_id)s
                            GROUP BY cu.curriculum_id, cu.name, de.credits, u.first_name, u.last_name, de.name, cu.rating, de.length, cu.semesters, cu.course_count
                            ORDER BY rating DESC
                            LIMIT 9;
                            """,
                            {"degree_id":degree_id}
            )
            self.connection.commit()
            try:
                curriculums = cursor.fetchall()
            except TypeError:
                curriculums = None
            return curriculums

    def update_rating(self, id, rating):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE curriculums"
                " SET rating=%(rating)s"
                " WHERE curriculum_id=%(curriculum_id)s ",
                {"curriculum_id": id, "rating": rating})
            self.connection.commit()
            return id

    def rename(self, id, name):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE curriculums"
                " SET name=%(name)s"
                " WHERE curriculum_id=%(curriculum_id)s ",
                {"curriculum_id": id, "name": name})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM curriculums WHERE curriculum_id=%(curriculum_id)s", {"curriculum_id": id})
            self.connection.commit()
            return id
