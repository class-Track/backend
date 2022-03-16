from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

class Courses:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='ec2-34-231-183-74.compute-1.amazonaws.com',
            database='ddetn88o84e93n',
            user='oisewifxugdivf',
            password='155a4e05bef9407085766f6326277a143b1aa857ed8210c48a4f4517947dd563'
        )

    def create(self, department_id, name, classification):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO courses (department_id, name, classification)"
                " VALUES ( %(department_id)s, %(name)s, %(classification)s)"
                " RETURNING course_id", {
                    "department_id": department_id, "name": name, "classification": classification}
            )
            self.connection.commit()
            course_id = cursor.fetchone()
            return course_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT department_id, name, classification FROM courses")
            self.connection.commit()
            users = cursor.fetchall()
            return users

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT course_id, department_id, name, classification FROM courses WHERE course_id=%(course_id)s",
                           {"course_id": id})
            self.connection.commit()
            try:
                user = cursor.fetchone()
            except TypeError:
                user = None
            return user

    def update(self, id, department_id, name, classification):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE courses"
                " SET department_id=%(department_id)s, name=%(name)s, classification=%(classification)s"
                " WHERE course_id=%(course_id)s ",
                {"course_id": id, "department_id": department_id, "name": name, "classification": classification})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM courses WHERE course_id=%(course_id)s", {"course_id": id})
            self.connection.commit()
            return id

    # Clean-Up
    def close_connection(self):
        self.connection.close()
