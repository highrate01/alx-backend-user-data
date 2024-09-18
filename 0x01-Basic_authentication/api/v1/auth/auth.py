#!/usr/bin/env python3
"""
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
