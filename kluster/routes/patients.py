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
def medications(user_id: str) -> tuple[Response, int] | Response | dict[Any, Any]:
    # print(type(user_id))
    date = request.args.get("date", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    if not isinstance(user_id, str):
        return jsonify(
            {
                "message": "couldn't Process Date or id",
                "Error": "Bad Request",
            }
        ), 400
    try:
        # Attempt to convert the date string to a datetime object
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # If there's an issue with the format or conversion, handle the error
        return jsonify({
            "message": "Invalid date format",
            "Error": "Bad Request",
        }), 400

    try:
        # GET THE ALL THE MEDICATIONS FOR A PATIENT WITHIN A GIVEN DATE
        medications_obj = Medication.query.filter(
            Medication.patient_id == user_id,
            Medication.start_date <= date,
            date <= Medication.end_date
        ).all()
        medication_dict = [meds.to_dict() for meds in medications_obj]
        return jsonify(
            {
                "message": "successful",
                "date": medication_dict
            }
        ), 200
    except Exception as exc:
        print(exc)
        return jsonify(
            {
                "message": "something went wrong",
                "error": "Internal server error"
            }
        ), 500

