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
    """ hey will send you back tokens that will allow you to authenticate to other Google endpoints on
    behalf of the use"""
    code = request.args.get("code")
    google_token_url = requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json().get(
        "token_endpoint"
    )
    # Prepare and send a request to get tokens, this requires https connection
    token_url, headers, body = client.prepare_token_request(
        google_token_url,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    # print(headers)
    # print(token_url)
    # print(body)
    # print(google_token_url)
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(os.environ.get("client_id"), os.environ.get("client_secret")),
    )

    # Parse the tokens for user information
    client.parse_request_body_response(json.dumps(token_response.json()))

    user_info_endpoint = requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json().get(
        "userinfo_endpoint"
    )
    uri, headers, body = client.add_token(user_info_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your database with the information you just got from Google
    # Begin user session by logging the user in
    login_user("")  # the user object

    # Send user back to homepage
    return redirect(url_for("index"))  # home page or whatever the flow allows

# WORKS
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


@auth.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))  # landing page