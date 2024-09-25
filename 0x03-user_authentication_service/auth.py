#!/usr/bin/env python3
"""
contains a hashed password function
"""
import bcrypt
from db import DB
from user import User
from typing import Optional
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """
    gen_salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), gen_salt)

    return hash_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> Optional[User]:
        """
        Registers user email
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            # If we reach here, it means a user with this email was found
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User doesn't exist, so we can create a new one
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
