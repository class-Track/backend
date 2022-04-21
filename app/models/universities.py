from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from app.dbconnection import dbconnection

load_dotenv()

class Universities:
    def __init__(self):
        self.connection = dbconnection().connection()

    def create(self, name, codification, state, country):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO universities (name, codification, state, country)"
                " VALUES ( %(name)s, %(codification)s, %(state)s, %(country)s)"
                " RETURNING university_id", {
                    "name": name, "codification": codification, "state": state, "country": country }
            )
            self.connection.commit()
            university_id = cursor.fetchone()
            return university_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT name, codification, state, country FROM universities")
            self.connection.commit()
            universities = cursor.fetchall()
            return universities

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT university_id, name, codification, state, country FROM universities WHERE university_id=%(university_id)s",
                           {"university_id": id})
            self.connection.commit()
            try:
                university = cursor.fetchone()
            except TypeError:
                university = None
            return university

    def update(self, id, name, codification, state, country):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE universities"
                " SET name=%(name)s, codification=%(codification)s, state=%(state)s, country=%(country)s"
                " WHERE university_id=%(university_id)s ",
                {"university_id": id, "name": name, "codification": codification, "state": state, "country": country})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM universities WHERE university_id=%(university_id)s", {"university_id": id})
            self.connection.commit()
            return id
