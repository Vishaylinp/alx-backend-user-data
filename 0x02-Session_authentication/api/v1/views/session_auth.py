#!/usr/bin/env python3
"""Flask view for session auth
"""
from api.v1.views import app_views
from flask import request, jsonify
import os
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def auth_session():
    """session auth
    """

    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    search_user = User.search({"email": email})
    if not search_user or search_user == []:
        return jsonify({"error": "no user found for this email"}), 404

    for user in search_user:
        if user.is_valid_password(password):
            from api.v1.app import auth
            sess_id = auth.create_session(user.id)
            repres = jsonify(user.to_json())
            sess_n = os.getenv("SESSION_NAME")
            repres.set_cookie(sess_n, sess_id)
            return repres

        return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def delete_session():
    """logout"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
