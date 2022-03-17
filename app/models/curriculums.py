from dotenv import load_dotenv
from flask import make_response
import os
import psycopg2
from flask.json import jsonify
from psycopg2.extras import RealDictCursor

load_dotenv()

class Curriculums:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='ec2-34-231-183-74.compute-1.amazonaws.com',
            database='ddetn88o84e93n',
            user='oisewifxugdivf',
            password='155a4e05bef9407085766f6326277a143b1aa857ed8210c48a4f4517947dd563'
        )

    def create(self, name, deptCode, user_id, department_id):
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
                "INSERT INTO curriculums (name, curriculum_id, user_id, department_id, rating)"
                " VALUES ( %(name)s, %(curriculum_id)s, %(user_id)s, %(department_id)s, 0)"
                " RETURNING curriculum_id", {
                    "name": name, "curriculum_id": curriculum_id, "user_id": user_id, "department_id": department_id, "rating": 0 }
            )
            self.connection.commit()
            curriculum_id = cursor.fetchone()
            return curriculum_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT name, curriculum_id, user_id, department_id, rating FROM curriculums")
            self.connection.commit()
            curriculums = cursor.fetchall()
            return curriculums

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT name, curriculum_id, user_id, department_id, rating FROM curriculums WHERE curriculum_id=%(curriculum_id)s",
                           {"curriculum_id": id})
            self.connection.commit()
            try:
                curriculum = cursor.fetchone()
            except TypeError:
                curriculum = None
            return curriculum

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

    # Clean-Up
    def close_connection(self):
        self.connection.close()
