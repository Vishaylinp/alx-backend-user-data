#!/usr/bin/env python3
"""Encryting Password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash password"""

    encode = password.encode()
    hashed_password = bcrypt.hashpw(encode, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate password"""
    validate = False
    encode = password.encode()
    if bcrypt.checkpw(encode, hashed_password):
        validate = True
    return validate
