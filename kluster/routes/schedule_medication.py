from flask import request, jsonify
from kluster.routes.patients import patients
from kluster.models.medication import Medication
from kluster.models.medication_logs import MedicationLogs
from scheduler.reminder import Reminder
from datetime import datetime, timedelta
from kluster import task_queue
from kluster.medication_log.medication_logs import create_medication_logs_async
from kluster import db
from kluster.helpers import mail_composer


@patients.route('/schedule/new_medication', methods=["POST"])
def new_medication_schedule():
    """schedule a new medication for a patient"""
    data = request.form
    try:
        assert (name := data.get("name", None, str)) is not None
        assert (patient_id := data.get("patient_id", None, str)) is not None
        assert (prescribed_by := data.get("prescribed_by", None, str)) is not None
        assert (dosage := data.get("dosage", None, str)) is not None
        # assert (start_date := data.get("start_date", None, str)) is not None
        # assert (end_date := data.get("end_date", None, str)) is not None
    except AssertionError as error:
        return jsonify({
            "message": "Bad Request",
            "error": f"Missing Field: {error}"
        }), 400
    start_date = datetime.now()
    end_date = start_date + timedelta(days=3)
    new_medication = Medication(name, patient_id, prescribed_by, dosage, start_date,
                                end_date)
    new_medication.insert()
    task = {
        "task_func": create_medication_logs_async,
        "args": [new_medication.patient_id, new_medication.id]
    }
    task_queue.put(task)
    if description := data.get("description", None, str):
        new_medication.description = description
        new_medication.update()
    # create a schedule
    try:
        new_reminder = Reminder(new_medication.name)
        new_reminder.start_schedule(interval=dosage, schedule_func=mail_composer, args=[new_medication.patient_id,
                                                                                        new_medication.id])
    except Exception as error:
        return jsonify({
            "message": "Medication could not be scheduled",
            "error": "internal server error"
        }), 500

    return jsonify({
        "message": "medication scheduled successfully",
        "data": new_medication.to_dict()
    }), 200


@patients.route("/schedule/<str:patient_id>")
def get_schedule(patient_id: str):
    """Get the schedule for a patient"""
    data = request.args
    try:
        assert isinstance(from_date := data.get("from", None, str), str)
        assert isinstance(to_date := data.get("to", None, str), str)
    except AssertionError:
        return jsonify({
            "message": "Bad request",
            "error": "query has to be a string"
        }), 400
    # query using the patient Id and date for the schedule
    scheduled_medication = MedicationLogs.query.filter(
        MedicationLogs.user_id == patient_id,
        db.or_(
            MedicationLogs.scheduled_time >= from_date,
            MedicationLogs.scheduled_time <= to_date
        ).order_by(MedicationLogs.scheduled_time.asc())
    )
    # temporary, extra processing is needed
    return jsonify({
        "message": "retrieved successfully",
        "data": [obj.to_dict() for obj in scheduled_medication]
    }), 200

