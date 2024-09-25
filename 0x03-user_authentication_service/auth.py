#!/usr/bin/env python3
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Optional


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hashes a password using bcrypt
        """
        gen_salt = bcrypt.gensalt()
        hash_pwd = bcrypt.hashpw(password.encode('utf-8'), gen_salt)
        return hash_pwd

    def register_user(self, email: str, password: str) -> User:
        """
        Registers user email
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)
        except InvalidRequestError:
            raise ValueError("Invalid email")

    def valid_login(self, email: str, password: str) -> bool:
        """
        validates user login
        """
        try:
            user = self._db.find_user_by(email=email)

            # Convert password to bytes and check hash
            pwd_bytes = password.encode('utf-8')

            hashed_password = user.hashed_password
            if isinstance(hashed_password, str):
                hashed_password = user.hashed_password.encode('utf-8')
            return bcrypt.checkpw(pwd_bytes, hashed_password)
        except NoResultFound:
            return False
