#!/usr/bin/env python3
"""
contains database class that stores authentication system
"""
from models.base import Base 


class UserSession(Base):
    """
    authentication system
    """
    def __init__(self, *args: list, **kwargs: dict):
        """initializer"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
