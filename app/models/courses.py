from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from app.dbconnection import dbconnection

load_dotenv()

class Courses:
    def __init__(self):
        self.connection = dbconnection().connection()

    def create(self, department_id, name, classification, credits):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO courses (department_id, name, classification, credits)"
                " VALUES ( %(department_id)s, %(name)s, %(classification)s, %(credits)s)"
                " RETURNING course_id", {
                    "department_id": department_id, "name": name, "classification": classification, "credits": credits}
            )
            self.connection.commit()
            course_id = cursor.fetchone()
            return course_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT course_id, department_id, name, classification, credits FROM courses")
            self.connection.commit()
            courses = cursor.fetchall()
            return courses

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT course_id, department_id, name, classification, credits FROM courses WHERE course_id=%(course_id)s",
                           {"course_id": id})
            self.connection.commit()
            try:
                course = cursor.fetchone()
            except TypeError:
                course = None
            return course

    def update(self, id, department_id, name, classification, credits):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE courses"
                " SET department_id=%(department_id)s, name=%(name)s, classification=%(classification)s, credits=%(credits)s"
                " WHERE course_id=%(course_id)s ",
                {"course_id": id, "department_id": department_id, "name": name, "classification": classification, "credits": credits})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM courses WHERE course_id=%(course_id)s", {"course_id": id})
            self.connection.commit()
            return id