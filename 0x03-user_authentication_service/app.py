#!/usr/bin/env python3
"""
contains flask routes
"""
from flask import (
        Flask,
        jsonify,
        request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
