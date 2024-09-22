#!/usr/bin/env python3
"""
handles all routes for the Session authentication.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os
from typing import Tuple
# from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    from api.v1.app import auth
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(getattr(user, 'id'))
    response = jsonify(user.to_json())
    session_name = os.getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_name, session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_logout():
    """
    Route to log out a user by deleting their session.
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
