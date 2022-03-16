from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

class Users:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='ec2-34-231-183-74.compute-1.amazonaws.com',
            database='ddetn88o84e93n',
            user='oisewifxugdivf',
            password='155a4e05bef9407085766f6326277a143b1aa857ed8210c48a4f4517947dd563'
        )

    def signUp(self, isAdmin, variant_id, first_name, last_name, email, password):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO users (first_name, last_name, email, password)"
                " VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s)"
                " RETURNING user_id", {
                    "first_name": first_name, "last_name": last_name, "email": email, "password": generate_password_hash(password, method='sha256') }
            )
            self.connection.commit()
            user_id = cursor.fetchone()
            
            if(isAdmin):
                cursor.execute(
                    "INSERT INTO admins (admin_id, university_id)"
                    " VALUES ( %(admin_id)s, %(university_id)s)"
                    " RETURNING admin_id", {
                        "admin_id": user_id['user_id'], "university_id": variant_id }
                )
            else:
                cursor.execute(
                    "INSERT INTO students (student_id, degree_id)"
                    " VALUES ( %(student_id)s, %(degree_id)s)"
                    " RETURNING student_id", {
                        "student_id": user_id['user_id'], "degree_id": variant_id }
                )
            self.connection.commit()

            return user_id

    def login(self, email, password):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT email, password FROM users WHERE email=%(email)s",
                {"email":email})
            self.connection.commit()
            try:
                user = cursor.fetchone()
            except TypeError:
                user = None
            
            if user and check_password_hash(user['password'], str(password)):
                user = user['email']
            else:
                user = None

            return user

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT first_name, last_name, email FROM users")
            self.connection.commit()
            users = cursor.fetchall()
            return users

    def readAdmin(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT user_id, university_id, first_name, last_name, email FROM users " 
                           "INNER JOIN admins ad ON(ad.admin_id = user_id) WHERE user_id=%(user_id)s",
                           {"user_id": id})
            self.connection.commit()
            try:
                user = cursor.fetchone()
            except TypeError:
                user = None
            return user

    def readStudent(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT user_id, degree_id, first_name, last_name, email FROM users " 
                           "INNER JOIN students st ON(st.student_id = user_id) WHERE user_id=%(user_id)s",
                           {"user_id": id})
            self.connection.commit()
            try:
                user = cursor.fetchone()
            except TypeError:
                user = None
            return user

    def update(self, id, isAdmin, variant_id, first_name, last_name, email, password):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE users"
                " SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s"
                " WHERE user_id=%(user_id)s ",
                {"user_id": id, "first_name": first_name, "last_name": last_name, "email": email, "password": password})
            self.connection.commit()

            if(isAdmin):
                cursor.execute(
                    "UPDATE admins"
                    " SET university_id=%(university_id)s"
                    " WHERE admin_id=%(admin_id)s ",
                    {"admin_id": id, "university_id": variant_id})
            else:
                 cursor.execute(
                    "UPDATE students"
                    " SET degree_id=%(degree_id)s"
                    " WHERE student_id=%(student_id)s ",
                    {"student_id": id, "degree_id": variant_id})               
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
