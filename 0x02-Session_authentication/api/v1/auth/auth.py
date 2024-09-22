#!/usr/bin/env python3
"""
contains class module
"""
from flask import request
from typing import List, TypeVar, Optional
import os


class Auth:
    """
    manage the API authentication.
    """
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """
        checks if api is required to access path
        """
        if path is None:
            return True
        if not excluded_paths or excluded_paths is None:
            return True
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path.rstrip('*')):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """
        checks authorizatrion header in the request
        """
        key = 'Authorization'

        if request is None:
            return None
        if key not in request.headers:
            return None
        return request.headers.get(key)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        checks user
        """
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            return User.get(user_id)
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
