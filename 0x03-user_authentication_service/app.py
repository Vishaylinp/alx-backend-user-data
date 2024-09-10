#!/usr/bin/env python3
"""app using flask"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def start() -> str:
    """return jsonify"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """user method"""

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        usr = AUTH.register_user(email, password)
        return jsonify({"email": usr.email, "message": "user created"})

    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
