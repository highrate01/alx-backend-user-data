#!/usr/bin/env python3
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Optional, Union
import uuid


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """
    gen_salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), gen_salt)
    return hash_pwd


def _generate_uuid() -> str:
    """
    returns a str rep of a newly generated uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers user email
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        except InvalidRequestError:
            raise ValueError("Invalid email")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login
        Args:
            email (str): User's email
            password (str): User's password
        Returns:
            bool: True if login is valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        pwd_bytes = password.encode('utf-8')
        if bcrypt.checkpw(pwd_bytes, user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """
        finds user corresponding to the email, generate
        a new UUID and store it in the database
        Args:
            email(str): user's email
        Returns:
            session_id(str): user's session id
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        session_id = _generate_uuid()
        update_user = self._db.update_user
        update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        finds user by session id and return
        corresponding user
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        updates the corresponding user’s session ID to None
        """
        if user_id is None:
            return None
        update_user = self._db.update_user
        update_user(user_id, session_id=None)
