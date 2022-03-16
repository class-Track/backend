from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

class History:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='ec2-34-231-183-74.compute-1.amazonaws.com',
            database='ddetn88o84e93n',
            user='oisewifxugdivf',
            password='155a4e05bef9407085766f6326277a143b1aa857ed8210c48a4f4517947dd563'
        )

    def create(self, user_id, curriculum_id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO history (user_id, curriculum_id)"
                " VALUES ( %(user_id)s, %(curriculum_id)s)"
                " RETURNING history_id", {
                    "user_id": user_id, "curriculum_id": curriculum_id}
            )
            self.connection.commit()
            history_id = cursor.fetchone()
            return history_id

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT user_id, curriculum_id FROM history")
            self.connection.commit()
            histories = cursor.fetchall()
            return histories

    def read(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT history_id, user_id, curriculum_id FROM history WHERE history_id=%(history_id)s",
                           {"history_id": id})
            self.connection.commit()
            try:
                history = cursor.fetchone()
            except TypeError:
                history = None
            return history

    def update(self, id, user_id, curriculum_id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE history"
                " SET user_id=%(user_id)s, curriculum_id=%(curriculum_id)s"
                " WHERE history_id=%(history_id)s ",
                {"history_id": id, "user_id": user_id, "curriculum_id": curriculum_id})
            self.connection.commit()
            return id

    def delete(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM history WHERE history_id=%(history_id)s", {"history_id": id})
            self.connection.commit()
            return id

    # Clean-Up
    def close_connection(self):
        self.connection.close()
