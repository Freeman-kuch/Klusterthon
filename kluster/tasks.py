from datetime import datetime, timedelta
from kluster import celery
from kluster.helpers import query_one_filtered
from kluster.models.medication import Medication
from kluster.models.medication_logs import MedicationLogs


@celery.task(name='create_medication_logs_async')
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