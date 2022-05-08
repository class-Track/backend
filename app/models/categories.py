from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from app.dbconnection import dbconnection

load_dotenv()

class Categories:
    def __init__(self):
        self.connection = dbconnection().connection()

    def create(self, name, classification):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO categories (name, classification)"
                " VALUES ( %(name)s, %(classification)s)"
                " RETURNING category_id", {
                    "name": name, "classification": classification}
            )
            self.connection.commit()
            category_id = cursor.fetchone()
            return category_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT category_id, name, classification FROM categories")
            self.connection.commit()
            categories = cursor.fetchall()
            return categories

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT category_id, name, classification FROM categories WHERE category_id=%(category_id)s",
                           {"category_id": id})
            self.connection.commit()
            try:
                course = cursor.fetchone()
            except TypeError:
                course = None
            return course

    def update(self, id, name, classification):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE categories"
                " SET name=%(name)s, classification=%(classification)s"
                " WHERE category_id=%(category_id)s ",
                {"category_id": id, "name": name, "classification": classification})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM categories WHERE category_id=%(category_id)s", {"category_id": id})
            self.connection.commit()
            return id