import os
from dotenv import load_dotenv

# The format this thing is looking for. Remember this is what DATABASE_URL has on Heroku
# postgres://USER:PASSWORD@HOST:PORT/DB_NAME

load_dotenv('conf/db_access.env')
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
