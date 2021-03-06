from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from app.dbconnection import dbconnection

load_dotenv()

class Degrees:
    def __init__(self):
        self.connection = dbconnection().connection()


    def create(self, name, department_id, length, credits):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO degrees (name, department_id, curriculum_sequence, length, credits)"
                " VALUES ( %(name)s, %(department_id)s, null, %(length)s, %(credits)s)"
                " RETURNING degree_id", {
                    "name": name, "department_id": department_id, "length": length, "credits": credits }
            )
            self.connection.commit()

            degree_id = cursor.fetchone().get("degree_id")
            curriculum_sequence = "{}_{}_admin".format(department_id, degree_id)

            cursor.execute(
                "UPDATE degrees"
                " SET curriculum_sequence=%(curriculum_sequence)s"
                " WHERE degree_id=%(degree_id)s ",
                {"curriculum_sequence": curriculum_sequence, "degree_id": degree_id})
            self.connection.commit()

            return degree_id

    def read_all_with_dept(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT dg.degree_id, dg.name as degree, dp.name as department FROM degrees dg "
                "INNER JOIN departments dp ON (dg.department_id = dp.department_id)")
            self.connection.commit()
            degrees = cursor.fetchall()
            return degrees

    
    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT degree_id, name, department_id, curriculum_sequence, length, credits FROM degrees")
            self.connection.commit()
            degrees = cursor.fetchall()
            return degrees

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT name, department_id, curriculum_sequence, length, credits FROM degrees WHERE degree_id=%(degree_id)s",
                           {"degree_id": id})
            self.connection.commit()
            try:
                degree = cursor.fetchone()
            except TypeError:
                degree = None
            return degree

    def update(self, id, name, department_id, curriculum_sequence, length, credits):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE degrees"
                " SET name=%(name)s, department_id=%(department_id)s, curriculum_sequence=%(curriculum_sequence)s, length=%(length)s, credits=%(credits)s"
                " WHERE degree_id=%(degree_id)s ",
                {"name": name, "degree_id": id, "department_id": department_id, "curriculum_sequence": curriculum_sequence, "length": length, "credits": credits})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM degrees WHERE degree_id=%(degree_id)s", {"degree_id": id})
            self.connection.commit()
            return id
