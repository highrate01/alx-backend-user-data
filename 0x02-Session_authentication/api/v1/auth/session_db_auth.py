#!/usr/bin/env python3
"""SessionDBAuth module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """Create and store new instance of UserSession"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the User ID by requesting UserSession in the database"""
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        user_session = user_sessions[0]
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the Session ID
        from the request cookie"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if user_sessions:
            user_sessions[0].remove()
            return True
        return False
