#!/usr/bin/env python3
"""Session Authentication
"""
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """class SessionAuth
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create asession
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        sess_id = uuid4()
        self.user_id_by_session_id[str(sess_id)] = user_id
        return str(sess_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """user id for session
        """

        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """current user
        """

        sess_user = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sess_user)
        user = User.get(user_id)
        return user
