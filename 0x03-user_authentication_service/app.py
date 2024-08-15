#!/usr/bin/env python3
"""Module to run Flask app
"""
from flask import (Flask, jsonify, Response, 
                   request, abort, make_response)
from auth import Auth
from typing import Optional, Tuple

AUTH = Auth()

app = Flask(__name__)


@app.route("/")
def home() -> Response:
    """
    Route to home
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route("/users", methods=["POST"])
def users() -> Response:
    """Registers users

    Returns:
        Response: JSON message with the status
    """
    if request.method == "POST":
        raw_email = request.form.get("email")
        raw_password = request.form.get("password")
        if not raw_email or not raw_password:
            abort(400)  # Missing email or password
        email = raw_email.strip()
        password = raw_password.strip()
        try:
            AUTH.register_user(email, password)
            message = jsonify({"email": email, "message": "user created"})
            return message
        except Exception:
            return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> Optional[Response]:
    """Handle user login
    Validates user credentials, generates a session ID,
    and sets a session cookie upon successful login.

    Returns:
        Optional[Response]: JSON response with appropriate message
    """
    try:
        raw_email = request.form.get("email")
        raw_password = request.form.get("password")
        if not raw_email or not raw_password:
            abort(401)  # Missing email or password

        email = raw_email.strip()
        password = raw_password.strip()

        if not AUTH.valid_login(email, password):
            abort(401)

        # Generate session ID and set the session cookie
        session_id = AUTH.create_session(email)
        if session_id:
            message = {"email": email, "message": "logged in"}
            response = make_response(jsonify(message), 200)
            response.set_cookie("session_id", session_id)
            return response
        else:
            abort(401)
    except Exception:
        abort(401)

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
