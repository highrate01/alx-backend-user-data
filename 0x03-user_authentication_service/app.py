#!/usr/bin/env python3
"""
contains flask routes
"""
from flask import (
        Flask,
        jsonify,
        request,
        abort,
        redirect,
        Response
        )
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome() -> str:
    """welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register() -> str:
    """
    register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        reg_user = AUTH.register_user(email, password)
        return jsonify({"email": reg_user.email,
                        "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    user login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(400)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)

        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

        return response, 200
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    user logout
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> Response:
    """
    get user profile
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    respond to reset password route
    """
    email = request.form.get('email')
    if not email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({
        "email": email,
        "reset_token": reset_token
        }), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Respond to password update request.

    This function handles the PUT request to reset a user's password.
    It expects the following form data:
    - email: The user's email address
    - new_password: The new password to set
    - reset_token: The token to validate the reset request

    Returns:
    - A JSON response with the user's email and a success message
    - HTTP 200 status code on success
    - HTTP 403 status code if the reset token is invalid

    Raises:
    - 403 Forbidden if the reset token is invalid or expired
    """
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    reset_token = request.form.get('reset_token')

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
