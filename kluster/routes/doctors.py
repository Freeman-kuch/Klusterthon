from flask import Blueprint

doctor = Blueprint("doctor", __name__, url_prefix="/api/v1/doctor")