from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

class Universities:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='ec2-34-231-183-74.compute-1.amazonaws.com',
            database='ddetn88o84e93n',
            user='oisewifxugdivf',
            password='155a4e05bef9407085766f6326277a143b1aa857ed8210c48a4f4517947dd563'
        )

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
            users = cursor.fetchall()
            return users

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT university_id, name, codification, state, country FROM universities WHERE university_id=%(university_id)s",
                           {"university_id": id})
            self.connection.commit()
            try:
                user = cursor.fetchone()
            except TypeError:
                user = None
            return user

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

    # Clean-Up
    def close_connection(self):
        self.connection.close()
