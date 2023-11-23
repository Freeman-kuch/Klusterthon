from flask import Blueprint

patients = Blueprint("patients", __name__, url_prefix="/api/v1/patients")