from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

class Departments:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='ec2-34-231-183-74.compute-1.amazonaws.com',
            database='ddetn88o84e93n',
            user='oisewifxugdivf',
            password='155a4e05bef9407085766f6326277a143b1aa857ed8210c48a4f4517947dd563'
        )

    def create(self, university_id, name, classification):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO departments (university_id, name, classification)"
                " VALUES ( %(university_id)s, %(name)s, %(classification)s)"
                " RETURNING department_id", {
                    "university_id": university_id, "name": name, "classification": classification }
            )
            self.connection.commit()
            department_id = cursor.fetchone()
            return department_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT university_id, name, classification FROM departments")
            self.connection.commit()
            departments = cursor.fetchall()
            return departments

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT university_id, name, classification FROM departments WHERE department_id=%(department_id)s",
                           {"department_id": id})
            self.connection.commit()
            try:
                department = cursor.fetchone()
            except TypeError:
                department = None
            return department

    def update(self, id, university_id, name, classification):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE departments"
                " SET university_id=%(university_id)s, name=%(name)s, classification=%(classification)s"
                " WHERE department_id=%(department_id)s ",
                {"department_id": id, "university_id": university_id, "name": name, "classification": classification})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM departments WHERE department_id=%(department_id)s", {"department_id": id})
            self.connection.commit()
            return id

    # Clean-Up
    def close_connection(self):
        self.connection.close()
