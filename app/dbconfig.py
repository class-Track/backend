import os
from dotenv import load_dotenv


# The format this thing is looking for. Remember this is what DATABASE_URL has on Heroku
# postgres://USER:PASSWORD@HOST:PORT/DB_NAME

neo4j_uri = os.getenv('NEO4J_URI')
neo4j_username = os.getenv('NEO4J_USERNAME')
neo4j_password = os.getenv('NEO4J_PASSWORD')

load_dotenv('backend/conf/db_access.env')
puri = os.environ.get('DATABASE_URL', "")

filler, credentials = puri.split("postgres://")
slice1, slice2 = credentials.split("@")
username, password = slice1.split(":")
host, slice3 = slice2.split(":")
port, database = slice3.split("/")

config = {
    'dbname': database,
    'user': username,
    'host': host,
    'password': password,
    'port': port
}
