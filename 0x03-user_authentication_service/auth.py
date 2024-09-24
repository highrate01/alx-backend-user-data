#!/usr/bin/env python3
"""
contains a hashed password function
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """
    gen_salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), gen_salt)

    return hash_pwd
