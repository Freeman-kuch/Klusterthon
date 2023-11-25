from flask import Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user, get_jwt_identity


from kluster import jwt
from kluster.helpers import convert_pic_to_link, query_one_filtered
from kluster.models.profiles import Profiles
from kluster.models.roles import Roles
from kluster.models.users import Users

profile = Blueprint("profile", __name__, url_prefix="/api/v1/profile")

profile.route("/", methods=["GET"])
def test():
    return "profile", 200