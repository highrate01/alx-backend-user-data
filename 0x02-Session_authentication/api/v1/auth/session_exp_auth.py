#!/usr/bin/env python3
"""
Contains the SessionExpAuth class
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Adds an  expiration date to session ID
    """
    def __init__(self):
        """initializer"""
        try:
            self.sess_dura = int(os.getenv('SESSION_DURATION'))
        except ValueError:
            self.sess_dura = 0

    def create_session(self, user_id=None):
        """
        Creates a session ID
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None
        session_dict = {
                "user_id": user_id,
                "created_at": datetime.utcnow()
                }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns user_id based on session_id
        """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)

        if session_dict is None:
            return None
        if self.sess_dura <= 0:
            return session_dict.get("user_id")
        created_at = session_dict.get("created_at")
        if created_at is None:
            return None

        exp_time = created_at + timedelta(seconds=self.sess_dura)
        if datetime.utcnow() >= exp_time:
            return None
        return session_dict.get("user_id")
