from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from app.dbconnection import dbconnection

load_dotenv()

class Departments:
    def __init__(self):
        self.connection = dbconnection().connection()

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
                "SELECT department_id, university_id, name, classification FROM departments")
            self.connection.commit()
            departments = cursor.fetchall()
            return departments

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT department_id, university_id, name, classification FROM departments WHERE department_id=%(department_id)s",
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
