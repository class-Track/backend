from app.dbconfig import config;
import psycopg2

class dbconnection:
    """Singleton DB Connection"""

    def __new__(cls):
        """New constructor, which ensures this is a singleton"""
        if not hasattr(cls, 'instance'): # If there's no instance, make sure there's an instance
            cls.instance = super(dbconnection, cls).__new__(cls)

        # If the instance that exists does not have a connection, or if the connection it does have is closed
        # then (re)connect to the DB.
        if not hasattr(cls.instance, 'db') or cls.db.closed > 0:
            cls.db = psycopg2.connect(**config)

        # Finally let's get the heck out of here
        return cls.instance

    def connection(self): return self.db

    def close(self): self.db.close()
