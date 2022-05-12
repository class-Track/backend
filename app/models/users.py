from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from app.dbconnection import dbconnection

load_dotenv()

class Users:
    def __init__(self):
        self.connection = dbconnection().connection()

    def signUp(self, isAdmin, variant_id, first_name, last_name, email, password):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT email FROM users WHERE email=%(email)s",
                {"email":email}
            )
            self.connection.commit()
            userExists = cursor.fetchone()

            if userExists:
                user_id = None
            else:
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
                "SELECT user_id, email, password FROM users WHERE email=%(email)s",
                {"email":email})
            self.connection.commit()
            try:
                user = cursor.fetchone()
            except TypeError:
                user = None
            
            if user and check_password_hash(user['password'], str(password)):
                user = { 'user_id': user['user_id'], 'email': user['email'] }
            else:
                user = None

            return user

    def read_all(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT user_id, first_name, last_name, email FROM users")
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

    def readStudentProfile(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT email, first_name, last_name, degrees.name AS degree_name, d.name AS department_name, u.name AS university_name "
                           "FROM students INNER JOIN users ON user_id = students.student_id NATURAL INNER JOIN degrees "
                           "NATURAL INNER JOIN departments d INNER JOIN universities u ON d.university_id = u.university_id "
                           "WHERE user_id=%(user_id)s",
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
                {"user_id": id, "first_name": first_name, "last_name": last_name, "email": email, "password": generate_password_hash(password, method='sha256') })
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
