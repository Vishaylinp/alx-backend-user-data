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

    def register_user(self, email: str, password: str) -> User:
        """register user"""

        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))

        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user

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

    def destroy_session(self, user_id: int) -> None:
        """destroy session"""

        if user_id is None:
            return None

        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """reset token
        """

        try:
            user = self._db.find_user_by(email=email)

        except NoResultFound:
            raise ValueError

        reset_t = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_t)
        return reset_t

    def update_password(self, reset_token: str, password: str) -> None:
        """update password"""

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            n_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=n_password,
                                 reset_token=None)

        except NoResultFound:
            raise ValueError
