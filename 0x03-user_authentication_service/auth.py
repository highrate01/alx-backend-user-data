#!/usr/bin/env python3
"""
contains a hashed password function
"""
import bcrypt
from db import DB
from user import User
from typing import Optional
from sqlalchemy.exc import NoResultFound


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
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """
    gen_salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), gen_salt)

    return hash_pwd
