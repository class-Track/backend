import uuid
from app.models.session import Session
from app.models.users import Users


class SessionManager:
    """Singleton session manager used across the app to manage who is signed in"""

    def __new__(cls):
        """New constructor, which ensures this is a singleton"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance

    __sessions__ = dict()
    """Sessions currently active"""

    def count(self):
        """count of currently logged in sessions"""
        return len(self.__sessions__)

    def login(self, user_id):
        """Adds a user to the list of active sessions. In essence, it logs them in. This is the last step in that
        process"""

        new_session = Session(user_id)

        while new_session.id in self.__sessions__.keys():  # Ensure this isn't a duplicate
            new_session.id = uuid.uuid4()

        self.__sessions__[str(new_session.id)] = new_session  # Actually add the session
        
        return new_session.id  # Return the session ID

    def find_session(self, session_id) -> Session:
        """Finds, extends, and returns a session with given ID. If the session is expired, it is removed."""
        if session_id is None:
            return None

        if session_id not in self.__sessions__.keys():
            return None  # If it doesn't exist, get the heck out

        if self.__sessions__[session_id].is_expired():
            self.__sessions__.pop(session_id)
            return None  # If it's an expired session, remove it and leave

        self.__sessions__[session_id].extend_session()  # Extend the session
        return self.__sessions__[session_id]  # Return it and adios

    def get_tied_user(self, session_id):
        """Finds the session using find_session and then gets the associated tied user from the DB"""
        s = self.find_session(session_id)

        if s is None:
            return None

        # TODO HEY REMEMBER TO UPDATE THIS WHEN WE UPDATE THE MODELS
        u = Users()
        session_user = u.read(s.user_id())
        u.close_connection()

        # We now return this as this

        return session_user, True

    def get_tied_student_or_admin(self,session_id):
        """Finds the session using find_session and gets the associated student or admin from the DB. returns
        a tuple with the student or admin, and a boolean determining if the user is a student or admin"""

        # This maybe should've been in the model all things considered. Something tells me a similar function will be
        # Needed later.

        s = self.find_session(session_id)

        if s is None:
            return None

        # TODO HEY REMEMBER TO UPDATE THIS WHEN WE UPDATE THE MODELS
        u = Users()
        session_user_as_student = u.readStudent(s.user_id())
        session_user_as_admin = u.readAdmin(s.user_id())
        u.close_connection()

        # We now return this as this

        if session_user_as_admin is None:
            return session_user_as_student, False
        else:
            return session_user_as_admin, True

    def logout(self, session_id):
        """Removes a session with given ID. In essence, logs a user out."""

        if session_id not in self.__sessions__.keys():
            return None  # Returns no session because there is no session to remove

        self.__sessions__.pop(session_id)
        return True  # Returns the session that is removed

