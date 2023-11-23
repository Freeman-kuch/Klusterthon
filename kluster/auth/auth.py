import datetime
import json
import os
import requests
from typing import Dict

from flask import Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user, get_jwt_identity
from oauthlib.oauth2 import WebApplicationClient
from werkzeug.security import generate_password_hash, check_password_hash

from kluster import jwt
from kluster.helpers import convert_pic_to_link, query_one_filtered
from kluster.models.profiles import Profiles
from kluster.models.roles import Roles
from kluster.models.users import Users

auth = Blueprint("authentication", __name__, url_prefix="/api/v1/auth")

# OAUTH2 client setup
client = WebApplicationClient(os.environ.get("client_id"))


@jwt.user_identity_loader
def user_identity_lookup(email: str) -> Dict | None:
    user = query_one_filtered(Users, email=email)
    return user if user else None


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data) -> Dict | None:
    identity = jwt_data["sub"]
    return query_one_filtered(Users, email=identity) or None


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
    picture_file = data.get('display_picture', None)

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
                         role_id=role.id, access_token=None, refresh_token=None)
        new_user.insert()
        if picture_file:
            picture_url = convert_pic_to_link(picture_file)
            new_user_profile = Profiles(user_id=new_user.id, first_name=first_name,
                                        last_name=last_name,
                                        date_of_birth=date_of_birth, gender=gender, display_picture=picture_url)
            new_user_profile.insert()
        new_user_profile = Profiles(user_id=new_user.id, first_name=first_name,
                                    last_name=last_name,
                                    date_of_birth=date_of_birth, gender=gender)
        new_user_profile.insert()
        return redirect(url_for("login"))
        # return jsonify({
        #     "message": "User created successfully",
        #     "data": new_user.format()
        # }), 201
    except Exception as error:
        return jsonify({
            "message": "Sign up failed",
            "error": "internal server error"
        }), 500


@auth.route("/login", methods=["POST"])
def login():
    req = request.form
    email = req.get("email")
    password = req.get("password")
    role = req.get("role")

    database_data = query_one_filtered(Users, email=email)

    if not email or not password or not role:
        return jsonify(
            {
                "error": "Bad Request",
                "message": "Bad request parameters"
            }
        ), 400
    if not database_data or check_password_hash(database_data["password"], password):
        return jsonify(
            {
                "message": "Invalid Email or Password",
                "error": "Bad Request"
            }
        ), 401
    try:
        access_token = create_access_token(
            identity=database_data["email"],
            fresh=True,
            expires_delta=datetime.timedelta(minutes=15),
            additional_claims={
                "role": database_data["role"]
            }
        )
        refresh_token = create_refresh_token(identity=database_data["email"])
        return jsonify(
            {
                "message": "login Successful",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            }
        ), 201
    except Exception as exc:
        jsonify(
            {
                "message": "something went wrong from the server",
                "error": "Internal Server Error"
            }
        ), 500


@auth.route("/me", methods=["GET"])
@jwt_required()
def me():
    return jsonify(
        id=current_user.id,
        email=current_user.email,
    )

@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)



@auth.delete("/logout")
@jwt_required(verify_type=False)
def logout():
    identity = current_user.id
    try:

        user = query_one_filtered(Users, id=identity)
        user["access_token"] = None
        user["refresh_token"] = None
        user.update()
        return jsonify(
            {
                "message":"you have been logged out",
            }
        ), 204

    except Exception as e:
        print(e)
        return jsonify(
            {
                "message":"something went Wrong will loggin this user out",
                "error": "Internal Server Error"
            }
        ), 500


@auth.route("/google-login/callback")
def callback():
    """ they will send you back tokens that will allow you to authenticate to other Google endpoints on
    behalf of the use"""
    code = request.args.get("code")
    google_token_url = requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json().get(
        "token_endpoint"
    )
    # Prepare and send a request with the code just gotten to get tokens, this requires https connection
    token_url, headers, body = client.prepare_token_request(
        google_token_url,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    # print(token_url, headers, body)
    token_response = requests.post(
        token_url,  # https://oauth2.googleapis.com/token
        headers=headers,  # {'Content-Type': 'application/x-www-form-urlencoded'}
        data=body,  # grant_type=authorization_code&client_id=87619606914-9ipquel4ov7ah31468gj3a2o0o2jr5rt.apps.
        # googleusercontent.com&code=4%2F0AfJohXl4XwZm8G-Cg2bKMjmqRB-mQbmvXCjKE4DjY
        # UKfXvSMUAAZeKB7NqzqX47SmvOPGA&redirect_uri=https%3A%2F%2F127.0.0.1%3A5000%2Fapi%2Fv1%2Fauth%2Fgoogle-login%2Fcallback

        auth=(os.environ.get("client_id"), os.environ.get("client_secret")),
    )  # This returns the access, refresh tokens from google.. the one associated the the user

    # Parse the tokens for user information
    f = client.parse_request_body_response(json.dumps(token_response.json()))
    # print(f["access_token"], f)

    user_info_endpoint = requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json().get(
        "userinfo_endpoint"
    )
    uri, headers, body = client.add_token(user_info_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    print(userinfo_response.json())
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        first_name = userinfo_response.json()["given_name"]
        last_name = userinfo_response.json()["family_name"]
    else:
        return "User email not available or not verified by Google.", 400
    try:

        new_user = Users(
            id=unique_id,
            email=users_email,
            password="",
            role_id="",
            refresh_token=f["refresh_token"],
            access_token=f["access_token"],
        )
        new_profile = Profiles(
            user_id=new_user.id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth="",
            display_picture=picture,
        )
    except:
        pass

    # Create a user in your database with the information you just got from Google
    # Begin user session by logging the user in
    login_user("")  # the user object  this will throw an error, because of the empty

    # Send user back to homepage
    return redirect(url_for("index"))  # home page or whatever the flow allows


# WORKS
@auth.route("/google-login")
def google_login():
    # Get Google authorization endpoint from OpenID configuration
    openid_configuration = requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json()
    authorization_endpoint = openid_configuration.get("authorization_endpoint")

    # Prepare login URI with required scopes, including "calendar"
    redirect_uri = request.base_url + "/callback"
    scopes = ["openid", "email", "profile", "https://www.googleapis.com/auth/calendar"]
    access_type = "offline"
    login_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=redirect_uri,
        scope=scopes,
        access_type=access_type
    )

    # Redirect to the Google login URI
    return redirect(login_uri)

