from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

class Degrees:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='ec2-34-231-183-74.compute-1.amazonaws.com',
            database='ddetn88o84e93n',
            user='oisewifxugdivf',
            password='155a4e05bef9407085766f6326277a143b1aa857ed8210c48a4f4517947dd563'
        )

    def create(self, department_id, curriculum_sequence, length, credits):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO degrees (department_id, curriculum_sequence, length, credits)"
                " VALUES ( %(department_id)s, %(curriculum_sequence)s, %(length)s, %(credits)s)"
                " RETURNING degree_id", {
                    "department_id": department_id, "curriculum_sequence": curriculum_sequence, "length": length, "credits": credits }
            )
            self.connection.commit()
            degree_id = cursor.fetchone()
            return degree_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT department_id, curriculum_sequence, length, credits FROM degrees")
            self.connection.commit()
            degrees = cursor.fetchall()
            return degrees

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT department_id, curriculum_sequence, length, credits FROM degrees WHERE degree_id=%(degree_id)s",
                           {"degree_id": id})
            self.connection.commit()
            try:
                degree = cursor.fetchone()
            except TypeError:
                degree = None
            return degree

    def update(self, id, department_id, curriculum_sequence, length, credits):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE degrees"
                " SET department_id=%(department_id)s, curriculum_sequence=%(curriculum_sequence)s, length=%(length)s, credits=%(credits)s"
                " WHERE degree_id=%(degree_id)s ",
                {"degree_id": id, "department_id": department_id, "curriculum_sequence": curriculum_sequence, "length": length, "credits": credits})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM degrees WHERE degree_id=%(degree_id)s", {"degree_id": id})
            self.connection.commit()
            return id

    # Clean-Up
    def close_connection(self):
        self.connection.close()
