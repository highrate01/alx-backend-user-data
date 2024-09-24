#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        returns a user object
        """
        user_dict = {
                'email': email,
                'hashed_password': hashed_password
                }
        user = User(**user_dict)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        returns the first row found in the users
        """
        if kwargs:
            for key in kwargs:
                if not hasattr(User, key):
                    raise InvalidRequestError()
                conditions = [getattr(
                    User, key) == value for key, value in kwargs.items()]

                user = self._session.query(User).filter(
                        and_(*conditions)).first()

                if not user:
                    raise NoResultFound()
                return user
        else:
            return None

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        updates the user details by id
        """
        if user_id:
            user = self.find_user_by(user_id=id)
            if kwargs:
                for key, value in kwargs.items():
                    if not hasattr(User, key):
                        raise ValueError
                    setattr(user, key, value)
                self._session.commit()
            return None
        return None
