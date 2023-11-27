from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from kluster.models.medication import Medication
#from kluster.models.medication_logs import MedicationLogs
from kluster.models.users import Users

from kluster.helpers import query_one_filtered
# from kluster import create_medication_logs_async


from datetime import datetime

medication_bp = Blueprint("medications", __name__, url_prefix="/api/v1/medications")


# CREATE (CREATE MEDICATION LOGS AS MEDICATIONS ARE PRESCRIBED)
@medication_bp.route("/<string:doctor_id>/<string:user_id>", methods=["POST"])
def create_medication(doctor_id, user_id):
    data = request.form
    user = query_one_filtered(Users, id=user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    medication = Medication(
        name=data.get('name'),
        patient_id=user_id, 
        prescribed_by=doctor_id,
        dosage=data.get('dosage'),
        start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d'),  # Parsing date string
        end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d'),  # Parsing date string
        description=data.get('description'),
        # has_taken=data.get('has_taken') == 'true'  # Assuming 'has_taken' is sent as a string
    )

    medication.insert()
    #task = create_medication_logs_async.apply_async(args=[user_id, medication.id])
    #create_medication_logs_async.delay(user_id, medication.id) 
    return jsonify({'message': 'Medication created successfully'}), 201

# UPDATE,
# def update_medications();


# DELETE

# GET
