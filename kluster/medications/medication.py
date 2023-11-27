from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from kluster.models.medication import Medication
from kluster.models.medication_logs import MedicationLogs
from kluster.models.users import Users
from kluster.helpers import query_one_filtered, query_all_filtered
from datetime import datetime, timedelta

from kluster.celery_utils import celery

medication_bp = Blueprint("medications", __name__, url_prefix="/api/v1/medications")


@celery.task
def create_medication_logs_async(user_id, medication_id):
    medication = query_one_filtered(Medication, id=medication_id, patient_id=user_id)

    if not medication:
        # If the medication is not found, you can either log this or handle it as needed
        return 'Medication not found'

    dosage = {
        "daily": 1,
        "bi_daily": 2,
        "tri_daily": 3,
        "quad_daily": 4,
    }

    medication_start = medication.start_date
    duration = medication.end_date - medication_start

    for day in range(duration.days + 1):  # +1 to include the end date
        day_date = medication_start + timedelta(days=day)
        for dose in range(dosage.get(medication.dosage, 1)):
            time_increment = timedelta(hours=24 / dosage.get(medication.dosage, 1))
            scheduled_time = datetime.combine(day_date, datetime.min.time()) + dose * time_increment

            # Create and save MedicationLog entry
            MedicationLogs(user_id=user_id, medication_id=medication.id, scheduled_time=scheduled_time).insert()

    return 'Medication logs scheduled successfully'


# CREATE (CREATE MEDICATION LOGS AS MEDICATIONS ARE PRESCRIBED)
@medication_bp.route("/<string:doctor_id>/<string:user_id>", methods=["POST"])
def create_medication(doctor_id, user_id):
    data = request.form
    user = query_one_filtered(Users, id=user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    medication = Medication(
        name=data.get('name'),
        patient_id=user_id,  # Corrected to use user_id directly
        prescribed_by=doctor_id,
        dosage=data.get('dosage'),
        start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d'),  # Parsing date string
        end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d'),  # Parsing date string
        description=data.get('description'),
        # has_taken=data.get('has_taken') == 'true'  # Assuming 'has_taken' is sent as a string
    )

    medication.insert()
    create_medication_logs_async.delay(user_id, medication.id)  # Trigger Celery task

    return jsonify({'message': 'Medication created successfully'}), 201

# UPDATE,
# def update_medications();


# DELETE

# GET
