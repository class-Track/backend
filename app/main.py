import os
import psycopg2
import gunicorn

from flask import Flask
from app.routes.universities_route import app_university_routes
from app.routes.degrees_route import app_degrees_routes
from app.routes.departments_route import app_departments_routes

app = Flask(__name__)

app.register_blueprint(app_university_routes)
app.register_blueprint(app_degrees_routes)
app.register_blueprint(app_departments_routes)

@app.route('/')
def hello():
    return 'Hello, Class Track!'

@app.route('/connect-db')
def connect():
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host='ec2-34-231-183-74.compute-1.amazonaws.com',
            database='ddetn88o84e93n',
            user='oisewifxugdivf',
            password='155a4e05bef9407085766f6326277a143b1aa857ed8210c48a4f4517947dd563'
        )

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if conn is not None:
            conn.close()
            message = 'PostgreSQL database version: '
            for string in db_version:
                message += str(string)
            return  message
