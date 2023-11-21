from flask import Blueprint, request, jsonify, redirect, url_for
from kluster.models.users import Users
from kluster.models.profiles import Profiles
from kluster.models.roles import Roles
from werkzeug.security import generate_password_hash
from kluster import login_manager


import json
import os
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests


auth = Blueprint("authentication", __name__, url_prefix="/api/v1/auth")

# OAUTH2 client setup
client = WebApplicationClient(os.environ.get("client_id"))

@auth.route('/sign_up', methods=['POST'])
def sign_up():
    """view function responsible for registering new user"""
    data = request.form
    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)
    email = data.get('email', None)
    password = data.get('password', None)
    gender = data.get('gender', None)
    date_of_birth = data.get('date_of_birth', None)
    role = data.get('role', None)

    try:
        assert first_name is not None
        assert last_name is not None
        assert email is not None
        assert password is not None
        assert gender is not None
        assert date_of_birth is not None
        assert role is not None
    except AssertionError:
        return jsonify({
            "message": "Bad Request",
            "error": "Missing Field"
        }), 400
    try:
        role = Roles.query.filter_by(role=role).first_or_404()
        hashed_password = generate_password_hash(password)
        new_user = Users(email=email, password=hashed_password,
                         role_id=role.id)
        new_user.insert()
        new_user_profile = Profiles(user_id=new_user.id,first_name=first_name,
                                    last_name=last_name,
                                    date_of_birth=date_of_birth, gender=gender)
        new_user_profile.insert()
        return jsonify({
            "message": "User created successfully",
            "data": new_user.format()
        }), 201
    except Exception as error:
        return jsonify({
            "message": "Sign up failed",
            "error": "internal server error"
        }), 500


@auth.route("/google-login/callback")
def callback():
    code = request.args.get("code")
    google_auth_url = requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json().get(
        "token_endpoint"
    )
    # now send the code back to google token endpoint
    return "something"

@auth.route("/google-login")
def google_login():
    google_auth_url = requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json().get(
        "authorization_endpoint"
    )
    login_uri = client.prepare_request_uri(
        google_auth_url,
        redirect_uri= request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(login_uri)