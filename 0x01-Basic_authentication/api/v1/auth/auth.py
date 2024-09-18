#!/usr/bin/env python3
"""
contains class module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    manage the API authentication.
    """
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """
        checks if api is required to access path
        """
        if not path or path not in excluded_paths:
            return True
        if not excluded_paths or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        if path and not path.endwith('/'):
            path = path + '/'
        return False

    def authorization_header(self, request=None) -> str:
        """
        checks authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        checks user
        """
        return None
