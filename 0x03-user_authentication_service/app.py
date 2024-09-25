#!/usr/bin/env python3
"""
contains flask routes
"""
from flask import (
        Flask,
        jsonify,
        request,
        abort,
        redirect
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


@app.route('/sesssions', methods=['DELETE'])
def logout() -> str:
    """
    user logout
    """
    session_id = request.cookies.get('seesion_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
