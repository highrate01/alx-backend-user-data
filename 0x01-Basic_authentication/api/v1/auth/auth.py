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
        if path is None:
            return True
        if not excluded_paths or excluded_paths is None:
            return True
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False
        return True

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
