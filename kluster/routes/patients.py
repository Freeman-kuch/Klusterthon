from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required
from kluster.helpers import query_one_filtered
from kluster.models.medication import Medication
from datetime import datetime
from typing import Dict, Tuple, Any

patients = Blueprint("patients", __name__, url_prefix="/api/v1/patients")

"""
MEDICATIONS
"""


@patients.route("/<user_id>/medications", methods=["GET"])
def medications(user_id: str) -> "tuple[Response, int] | Response | dict[Any, Any]":
    """
    Retrieves medication information for a specific patient based on the provided user ID and date.

    Args:
        user_id (str): The ID of the patient for whom to retrieve medication information.

    Returns:
        tuple[Response, int] | Response | dict[Any, Any]: If successful, returns a JSON response with a success message and a list of medication dictionaries.
            If the user_id or date is invalid, returns a JSON response with an error message and a 400 Bad Request status code.
            If an internal server error occurs, returns a JSON response with an error message and a 500 Internal Server Error status code.
    """
    date = request.args.get("date", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    if not isinstance(user_id, str):
        return jsonify(
            {
                "message": "couldn't Process Date or id",
                "Error": "Bad Request",
            }
        ), 400
    try:
        date_val = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({
            "message": "Invalid date format",
            "Error": "Bad Request",
        }), 400

    try:
        # Change the return of the prescribed by to show the name of the doctor
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



@patients.route("/<user_id>/medications/<medication_id>", methods=["GET", "DELETE"])
def medication(user_id: str, medication_id: str) -> "tuple[Response, int] | Response | dict[Any, Any]":
    """Gets a users medication by an indicated medication id

    Args:
        user_id (str): The ID of the  Patiend
        medication_id (str): The ID of the medication to be gotten

    Returns:
        tuple[Response, int] | Response | dict[Any, Any]: _description_
    """
    if not isinstance(user_id, str) or not isinstance(medication_id, str):
        return jsonify(
            {
                "message": "Invalid ID type passed, expecting UUID",
                "error": "Bad Request"
            }
        )
    if request.method == "GET":
        try:
            medication_obj = Medication.query.filter(
                Medication.id == medication_id,
                Medication.patient_id == user_id,
                ).first_or_404("The Requested Medication was not found.")
            return jsonify({
                "data": medication_obj.to_dict(),
                "message": "successful"
                }
                ), 200
        except Exception as exc:
            print(exc)
            return jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "Something went wrong"
                }
            ), 500
    
    try:
        medication_obj = Medication.query.filter(
            Medication.id == medication_id,
            Medication.patient_id == user_id,
        ).first_or_404("Not Found")
        print(medication_obj.to_dict())
        print(type(medication_obj))
        medication_obj.delete()
        return jsonify(
            {
                "message": "deleted"
            }
        ), 204
    except Exception as e:
        print(e)
        return jsonify(
            { 
                "error": "Something went wrong",
                "message": "Internal Server Error" 
             }
            ), 500

from kluster.routes.schedule_medication import *
