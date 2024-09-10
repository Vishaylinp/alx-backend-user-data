#!/usr/bin/env python3
"""hash passs"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> str:
    """hash password method"""

    hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hash_password


def _generate_uuid() -> str:
    """generate unique id"""

    u_id = uuid4()
    return str(u_id)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """register user"""

        try:
            self._db.find_user_by(email=email)

        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

        else:
            raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """validate login"""

        try:
            user = self._db.find_user_by(email=email)

        except NoResultFound:
            return False

        else:
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create session
        """

        try:
            user = self._db.find_user_by(email=email)

        except NoResultFound:
            return None

        sess_id = _generate_uuid()
        self._db.update_user(user.id, session_id=sess_id)
        return sess_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user"""

        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)

        except NoResultFound:
            return None

        return user
