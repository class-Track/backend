import os
import psycopg2
import gunicorn

from flask import Flask
from .neo4j import init_driver

def create_app(test_config=None):
    from app.routes.universities_routes import app_universities_routes
    from app.routes.degrees_routes import app_degrees_routes
    from app.routes.curriculum_ratings_routes import app_curriculum_ratings_routes
    from app.routes.departments_route import app_departments_routes
    from app.routes.user_route import app_users_routes
    from app.routes.history_route import app_history_routes
    from app.routes.curriculums_route import app_curriculum_routes
    from app.routes.courses_route import app_course_routes
    from app.routes.curriculum_graph_route import app_curr_graph__routes
    from flask_cors import CORS, cross_origin

    app = Flask(__name__)
    CORS(app)

    app.config.from_mapping(
        NEO4J_URI=os.getenv('NEO4J_URI'),
        NEO4J_USERNAME=os.getenv('NEO4J_USERNAME'),
        NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD'),
        NEO4J_DATABASE=os.getenv('NEO4J_DATABASE'),
    )

    with app.app_context():
        init_driver(
            app.config.get('NEO4J_URI'),
            app.config.get('NEO4J_USERNAME'),
            app.config.get('NEO4J_PASSWORD'),
        )

    app.register_blueprint(app_universities_routes)
    app.register_blueprint(app_degrees_routes)
    app.register_blueprint(app_curriculum_ratings_routes)
    app.register_blueprint(app_departments_routes)
    app.register_blueprint(app_users_routes)
    app.register_blueprint(app_history_routes)
    app.register_blueprint(app_curriculum_routes)
    app.register_blueprint(app_course_routes)
    app.register_blueprint(app_curr_graph__routes)

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

    return app



