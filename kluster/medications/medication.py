from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from kluster.models.medication import Medication
from kluster.models.medication_logs import MedicationLogs
from kluster.models.users import Users
from kluster.helpers import query_one_filtered, query_all_filtered

medication_bp = Blueprint("medications", __name__, url_prefix="/api/v1/medications")

#CREATE(CREATE MEDICATION LOGS AS MEDICATIONS ARE PRESCRIBED), 
@medication_bp.route("string:doctor_id/<>/<string:user_id>", methods=["POST"])
def create_medication(doctor_id, user_id):
    data = request.form
    user = query_one_filtered(Users, id=user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    medication = Medication(
        name=data.get('name', None),
        patient_id= data.get(user_id, None),
        prescribed_by=doctor_id,
        dosage=data.get('dosage', None),
        start_date=data.get('start_date', None),
        end_date=data.get('end_date', None),
        description=data.get('description', None),
        has_taken=data.get('has_taken', None)
    )

    medication.insert()
    #call asyn function to create logs
    return jsonify({'message': 'Medication created successfully'}), 201


#UPDATE, 
#def update_medications();
    

#DELETE 

#GET