from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

class Users:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='ec2-34-231-183-74.compute-1.amazonaws.com',
            database='ddetn88o84e93n',
            user='oisewifxugdivf',
            password='155a4e05bef9407085766f6326277a143b1aa857ed8210c48a4f4517947dd563'
        )

    def create(self, degree_id, first_name, last_name, email, password):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO users (degree_id, first_name, last_name, email, password)"
                " VALUES ( %(degree_id)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s)"
                " RETURNING user_id", {
                    "degree_id": degree_id, "first_name": first_name, "last_name": last_name, "email": email, "password": password }
            )
            self.connection.commit()
            user_id = cursor.fetchone()
            return user_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT degree_id, first_name, last_name, email, password FROM users")
            self.connection.commit()
            users = cursor.fetchall()
            return users

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT user_id, degree_id, first_name, last_name, email, password FROM users WHERE user_id=%(user_id)s",
                           {"user_id": id})
            self.connection.commit()
            try:
                user = cursor.fetchone()
            except TypeError:
                user = None
            return user

    def update(self, id, degree_id, first_name, last_name, email, password):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE users"
                " SET degree_id=%(degree_id)s, first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s"
                " WHERE user_id=%(user_id)s ",
                {"user_id": id, "degree_id": degree_id, "first_name": first_name, "last_name": last_name, "email": email, "password": password})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM users WHERE user_id=%(user_id)s", {"user_id": id})
            self.connection.commit()
            return id

    # Clean-Up
    def close_connection(self):
        self.connection.close()
