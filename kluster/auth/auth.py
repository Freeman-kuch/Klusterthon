from flask import Blueprint

auth = Blueprint("authentication", __name__, url_prefix="/api/v1/auth")