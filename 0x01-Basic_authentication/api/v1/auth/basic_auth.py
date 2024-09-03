#!/usr/bin/env python3
"""Basic Auth
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """class that inherits from Auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """"extract authorization header"""

        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        hold = authorization_header.split(" ")[-1]
        return hold

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decode base64"""

        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            convert_to_bytes = base64_authorization_header.encode("utf-8")
            decodes = base64.b64decode(convert_to_bytes)
            return decodes.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """user credentials"""

        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        email, user_password = decoded_base64_authorization_header.split(":")
        return (email, user_password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user object from credentials"""

        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            user_search = User.search({"email": user_email})
        except Exception:
            return None

        for user in user_search:
            if user.is_valid_password(user_pwd):
                return user
        return None
