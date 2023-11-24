from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required
from kluster.helpers import query_all_filtered
from kluster.models.medication import Medication
from datetime import datetime
from typing import Dict, Tuple, Any

patients = Blueprint("patients", __name__, url_prefix="/api/v1/patients")

"""
MEDICATIONS
"""


@patients.route("/<user_id>/medications", methods=["GET"])
# @jwt_required()
def medications(user_id: str) -> tuple[Response, int] | dict[Any, Any]:
    # print(type(user_id))
    date = request.args.get("date", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    print(type(date))
    if not isinstance(user_id, str):
        return jsonify(
            {
                "message": "couldn't Process Date or id",
                "Error": "Bad Request",
            }
        ), 400

    # try:
    medications_obj = query_all_filtered(Medication, patient_id=user_id)
    print(medications_obj)
    return {}
