import uuid
from datetime import datetime, timedelta, date


class Session:
    """Class for each individual session."""

    id = uuid.uuid4()  # Generates a random UUID when instantiating the Session
    """ID of this session. This is what the frontend receives and uses as a key to do stuff"""

    _expiration_date_ = datetime.min  # This is
    """Expiration date of this session. If the time is past this date, this session is expired, and cannot be used!"""

    def expiration_date(self):
        """Public accessor for the expiration date"""
        return self._expiration_date_

    _user_id_ = ""
    """ID of the user attached to this session."""

    def user_id(self):
        """public accessor for the user ID"""
        return self._user_id_

    def is_expired(self):
        """boolean that determines if this session is already expired"""
        return datetime.now > self._expiration_date_

    def __init__(self, user_id):
        """Constructor for a session for given user_id"""
        self._user_id_ = user_id
        self.extend_session()

    def extend_session(self):
        """Extends a session by 7 days"""
        self._expiration_date_ = date.today() + timedelta(days=7)

    def equals(self, other_session):
        """checks if this session equals another session"""
        return self.id == other_session.id
