#!/usr/bin/env python3
"""API authentication.
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """requires authorization
        """
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        for paths in excluded_paths:
            if paths.startswith(path):
                return False
            elif path.startswith(paths):
                return False
            elif paths[-1] == "*":
                if path.startswith(paths[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """"authorise header
        """
        if request is None:
            return None

        header_key = request.headers.get("Authorization")

        if header_key is None:
            return None
        return header_key

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None

    def session_cookie(self, request=None):
        """session cookie generator
        """

        if request is None:
            return None

        session_n = os.getenv("SESSION_NAME")
        return request.cookies.get(session_n)
